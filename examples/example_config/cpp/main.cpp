#include "config.pb.h"
#include "schema/super_mutation.pb.h" // Generated plugin header
#include <fstream>
#include <google/protobuf/util/json_util.h>
#include <iostream>
#include <sstream>

int main(int argc, char **argv) {
  if (argc < 2) {
    std::cerr << "Usage: " << argv[0] << " <path_to_json_config>\n";
    return 1;
  }

  htp::config::OptimizationConfig config;

  // 1. Read JSON file
  std::ifstream input(argv[1]);
  std::stringstream buffer;
  buffer << input.rdbuf();

  // 2. Parse JSON (Protobuf automatically resolves Any types registered in the
  // binary)
  auto status =
      google::protobuf::util::JsonStringToMessage(buffer.str(), &config);
  if (!status.ok()) {
    std::cerr << "Failed to parse JSON: " << status.message() << "\n";
    return 1;
  }

  std::cout << "[C++] Loaded base iterations: " << config.iterations() << "\n";

  // 3. Unpack the polymorphic 'Any' mutation_params safely
  if (config.has_mutation_params()) {
    htp::plugins::SuperMutationParams super_params;
    if (config.mutation_params().UnpackTo(&super_params)) {
      std::cout << "[C++] Unpacked SuperMutationParams successfully!\n";
      std::cout << "[C++]   - Adaptive Rate: " << super_params.adaptive_rate()
                << "\n";
      std::cout << "[C++]   - Cross-over: "
                << (super_params.chromosomal_crossover() ? "true" : "false")
                << "\n";
    } else {
      std::cerr << "[C++] Failed to unpack mutation_params into "
                   "SuperMutationParams\n";
    }
  }

  return 0;
}
