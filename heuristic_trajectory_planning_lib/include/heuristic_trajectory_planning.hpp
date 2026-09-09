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
  std::string json_str = buffer.str();

  google::protobuf::util::JsonParseOptions options;
  auto status =
      google::protobuf::util::JsonStringToMessage(json_str, &config, options);

  if (!status.ok()) {
    std::cerr << "Failed to parse JSON config: " << status.message() << "\n";
    return;
  }

  std::cout << "Iterations: " << config.iterations() << "\n";
  std::cout << "Epsilon: " << config.epsilon() << "\n";

  switch (config.model_case()) {
  case htp::config::OptimizationConfig::kModelLinear:
    std::cout << "Slope: " << config.model_linear().slope() << "\n";
    break;
  case htp::config::OptimizationConfig::kModelNonLinear:
    std::cout << "Degree: " << config.model_non_linear().polynomial_degree()
              << "\n";
    break;
  default:
    std::cout << "No model configured\n";
  }
}
