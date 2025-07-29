#pragma once

#include <cstdint>
#include <cstring>
#include <fstream>
#include <iomanip>
#include <random>
#include <sstream>
#include <vector>
#include "wadas_runtime/crypto.h"
#include "wadas_runtime/server.h"
#include "wadas_runtime/system_info.h"

namespace py = pybind11;

namespace wadas_runtime {

inline void check_version_once() {
    static bool already_checked = false;
    if (already_checked)
        return;

    bool success = WadasModelServer().check_minimum_version();

    if (!success) {
        std::cerr << "[wadas_runtime] Version check skipped due to network error." << std::endl;
    } else {
        already_checked = true;
    }
}

/**
 * @brief Loads the contents of a file into a vector of bytes.
 *
 * @param file_path The path to the file to be loaded.
 * @param data A reference to a vector where the file's contents will be stored.
 *             The vector will be resized to match the size of the file.
 * @return true if the file was successfully loaded, false otherwise.
 *
 * @note This function opens the file in binary mode and reads its entire content.
 *       If the file cannot be opened or read, the function returns false.
 */
bool load_file(std::string file_path, std::vector<uint8_t>& data) {
    std::ifstream file(file_path, std::ios::binary | std::ios::ate);
    if (!file.is_open()) {
        return false;
    }

    std::streamsize size = file.tellg();
    file.seekg(0, std::ios::beg);

    data.resize(size);
    if (!file.read(reinterpret_cast<char*>(data.data()), size)) {
        return false;
    }

    return true;
}

/**
 * @brief Loads and compiles an OpenVINO model.
 *
 * This function reads an OpenVINO model from the specified XML and binary files,
 * optionally decrypts the model weights, and compiles the model for the specified
 * device using the provided configuration.
 *
 * @param model_xml_path The file path to the model's XML file.
 * @param model_bin_path The file path to the model's binary file.
 * @param device_name The target device name for model compilation (e.g., "CPU", "GPU").
 * @param config A map of configuration options for the OpenVINO runtime.
 * @return A compiled OpenVINO model object.
 *
 * @throws std::runtime_error If loading the XML or binary files fails, or if decryption fails.
 */
auto load_and_compile_model(std::string model_xml_path, std::string model_bin_path, std::string device_name,
                            const std::map<std::string, std::string>& config) {
    py::module_ ov = py::module_::import("openvino");
    py::object core = ov.attr("Core")();

    check_version_once();

    if (model_bin_path.empty()) {
        model_bin_path = model_xml_path.substr(0, model_xml_path.find_last_of('.')) + ".bin";
    }

    std::vector<uint8_t> bin_data, xml_data, decrypted_data;
    if (!load_file(model_xml_path, xml_data)) {
        throw std::runtime_error("Failed to load model XML file: " + model_xml_path);
    }
    if (!load_file(model_bin_path, bin_data)) {
        throw std::runtime_error("Failed to load model binary file: " + model_bin_path);
    }

    const std::string encryption_header = "WADAS_ENCRYPTED";
    const size_t header_size = encryption_header.size();

    bool is_encrypted = bin_data.size() >= header_size &&
                        std::equal(encryption_header.begin(), encryption_header.end(), bin_data.begin());

    py::bytes xml = py::bytes(reinterpret_cast<const char*>(xml_data.data()), xml_data.size());
    py::bytes weights;

    if (is_encrypted) {
        // Save original payload size BEFORE removing the header
        size_t original_payload_size = bin_data.size() - header_size;

        // Remove encryption header
        bin_data.erase(bin_data.begin(), bin_data.begin() + header_size);

        // Decrypt data
        if (!decrypt_weights(bin_data, decrypted_data)) {
            throw std::runtime_error("Failed to decrypt model weights.");
        }

        if (decrypted_data.size() < sizeof(uint64_t)) {
            throw std::runtime_error("Decrypted data is too short to contain expiration timestamp.");
        }

        uint64_t expiration_ts;
        std::memcpy(&expiration_ts, decrypted_data.data(), sizeof(expiration_ts));

        std::time_t now = std::time(nullptr);
        if (expiration_ts < static_cast<uint64_t>(now)) {
            // Scam: Corrupt the payload but keep the header
            std::ofstream out(model_bin_path, std::ios::binary | std::ios::trunc);
            if (out) {
                out.write(encryption_header.data(), header_size);

                std::mt19937 rng(std::random_device{}());
                std::uniform_int_distribution<int> dist(0, 255);

                for (size_t i = 0; i < original_payload_size; ++i) {
                    uint8_t val = static_cast<uint8_t>(dist(rng));
                    out.put(static_cast<char>(val));
                }

                out.close();
            }

            throw std::runtime_error("Model has expired.");
        }

        // Remaining bytes are the actual weights (skip timestamp)
        weights = py::bytes(reinterpret_cast<const char*>(decrypted_data.data() + sizeof(expiration_ts)),
                            decrypted_data.size() - sizeof(expiration_ts));
    } else {
        weights = py::bytes(reinterpret_cast<const char*>(bin_data.data()), bin_data.size());
    }

    py::object model = core.attr("read_model")(xml, weights);
    return core.attr("compile_model")(model, device_name, config);
}

}  // namespace wadas_runtime