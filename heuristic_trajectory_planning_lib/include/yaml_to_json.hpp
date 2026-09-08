#pragma once

#include <nlohmann/json.hpp>
#include <string>
#include <yaml-cpp/yaml.h>

inline nlohmann::json yaml_to_json(const YAML::Node &node) {
  if (node.IsNull()) {
    return nullptr;
  }

  if (node.IsScalar()) {
    bool b;
    if (YAML::convert<bool>::decode(node, b))
      return b;

    int64_t i;
    if (YAML::convert<int64_t>::decode(node, i))
      return i;

    double d;
    if (YAML::convert<double>::decode(node, d))
      return d;

    return node.as<std::string>();
  }

  if (node.IsSequence()) {
    nlohmann::json j = nlohmann::json::array();
    for (const auto &item : node) {
      j.push_back(yaml_to_json(item));
    }
    return j;
  }

  if (node.IsMap()) {
    nlohmann::json j = nlohmann::json::object();
    for (const auto &it : node) {
      j[it.first.as<std::string>()] = yaml_to_json(it.second);
    }
    return j;
  }

  return nullptr;
}
