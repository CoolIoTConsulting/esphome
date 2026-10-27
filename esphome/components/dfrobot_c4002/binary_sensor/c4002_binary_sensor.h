#pragma once

#include "../dfrobot_c4002.h"
#include "esphome/components/binary_sensor/binary_sensor.h"

namespace esphome {
namespace dfrobot_c4002 {

class C4002BinarySensor : public C4002Listener, public Component {
 public:
  void set_presence_binary_sensor(binary_sensor::BinarySensor *presence) { this->presence_ = presence; }

  void on_target_status(uint8_t state) override {
    if (this->presence_ == nullptr)
      return;
    // Ignore error frames so a bad read doesn't flip the sensor.
    if (state == TARGET_ERROR)
      return;
    // The sensor reports presence both for a stationary (EXIST) and a moving (MOVE) target.
    bool present = (state == EXIST || state == MOVE);
    if (!this->presence_->has_state() || this->presence_->state != present) {
      this->presence_->publish_state(present);
    }
  }

 protected:
  binary_sensor::BinarySensor *presence_{nullptr};
};

}  // namespace dfrobot_c4002
}  // namespace esphome