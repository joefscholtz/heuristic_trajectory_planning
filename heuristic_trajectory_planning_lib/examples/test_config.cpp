#include "config.pb.h"
#include <fstream>
#include <google/protobuf/util/json_util.h>
#include <iostream>
#include <sstream>

void load_config(const std::string &filepath) {
  htp::config::OptimizationConfig config;

  std::ifstream input(filepath);
  if (!input.is_open()) {
    std::cerr << "Failed to open config file: " << filepath << "\n";
    return;
  }
  std::stringstream buffer;
  buffer << input.rdbuf();

  auto status =
      google::protobuf::util::JsonStringToMessage(buffer.str(), &config);
  if (!status.ok()) {
    std::cerr << "Failed to parse JSON config: " << status.message() << "\n";
    return;
  }

  std::cout << "[C++] Iterations: " << config.iterations() << "\n";
  std::cout << "[C++] Epsilon: " << config.epsilon() << "\n";

  switch (config.model_case()) {
  case htp::config::OptimizationConfig::kModelLinear:
    std::cout << "[C++] Model: Linear (slope: " << config.model_linear().slope()
              << ")\n";
    break;
  case htp::config::OptimizationConfig::kModelNonLinear:
    std::cout << "[C++] Model: NonLinear (degree: "
              << config.model_non_linear().polynomial_degree() << ")\n";
    break;
  default:
    std::cout << "[C++] No model configured\n";
  }
}

int main(int argc, char **argv) {
  if (argc < 2) {
    std::cerr << "Usage: " << argv[0] << " <path_to_json_config>\n";
    return 1;
  }
  load_config(argv[1]);
  return 0;
}
