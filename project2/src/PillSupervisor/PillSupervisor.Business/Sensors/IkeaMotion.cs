using MQTTnet;
using MQTTnet.Client;
using Newtonsoft.Json;

namespace PillSupervisor.Business.Sensors;

public class IkeaMotion : Sensor
{
    public class IkeaMotionData
    {
        public int? Battery { get; set; }
        public bool? Occupancy { get; set; }
        public int?  Requested_brightness_level { get; set; }
        public int?  Requested_brightness_percent { get; set; }
        public bool? Illuminance_above_threshold { get; set; }
        public int? Linkquality { get; set; }
    }

    public IkeaMotionData Data { get; set; }
    public IkeaMotion(MqttFactory mqttFactory, MqttClient mqttClient, string rootTopic, string id, string name) : 
        base(mqttFactory, mqttClient, rootTopic, id, name)
    {
        Data = new IkeaMotionData();
    }

    public override void Update(string payload)
    {
        var data = JsonConvert.DeserializeObject<IkeaMotionData>(payload);

        Data.Battery = data.Battery ?? Data.Battery;
        Data.Occupancy = data.Occupancy ?? Data.Occupancy;
        Data.Requested_brightness_level = data.Requested_brightness_level ?? Data.Requested_brightness_level;
        Data.Requested_brightness_percent = data.Requested_brightness_percent ?? Data.Requested_brightness_percent;
        Data.Illuminance_above_threshold = data.Illuminance_above_threshold ?? Data.Illuminance_above_threshold;
        Data.Linkquality = data.Linkquality ?? Data.Linkquality;
    }
}