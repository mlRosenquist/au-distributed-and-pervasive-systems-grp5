using System.Drawing;
using MQTTnet;
using MQTTnet.Client;
using Newtonsoft.Json;
using PillSupervisor.Business.Sensors;

namespace PillSupervisor.Business.Actuators;

public class LightStrip : Actuator
{
    public class UpdateData
    {
        public string? state { get; set; }
    }
    
    public class LightStripData : ActuatorData
    {
        public string? State { get; set; }
        public string? Color_mode { get; set; }
        public int? Linkquality  { get; set; }
        public UpdateData? Update { get; set; }
        public bool? Update_Available { get; set; }
    }

    public LightStripData Data { get; set; }
    public LightStrip(MqttFactory mqttFactory, MqttClient mqttClient, string rootTopic, string id, string name) : 
        base(mqttFactory, mqttClient, rootTopic, id, name)
    {
        Data = new LightStripData();
    }
    
    public override void Update(string payload)
    {
        var data = JsonConvert.DeserializeObject<LightStripData>(payload);

        Data.State = data.State ?? Data.State;
        Data.Color_mode = data.Color_mode ?? Data.Color_mode;
        Data.Linkquality = data.Linkquality ?? Data.Linkquality;
        Data.Update = data.Update ?? Data.Update;
        Data.Update_Available = data.Update_Available ?? Data.Update_Available;
    }

    public void Get()
    {
        var applicationMessage = new MqttApplicationMessageBuilder()
            .WithTopic($"{RootTopic + Id}/get")
            .WithPayload("{\"state\": \"\"}")
            .Build();

        MqttClient.PublishAsync(applicationMessage, CancellationToken.None);
    }
    
    public void TurnOn(int brightness = 200, string hexColor = "#EE401A")
    {
        var applicationMessage = new MqttApplicationMessageBuilder()
            .WithTopic($"{RootTopic + Id}/set")
            .WithPayload("{" +
                         "\"state\": \"ON\", \n" +
                         $"\"brightness\": \"{brightness}\", \n" +
                         $"\"color\": {{\"hex\": \"{hexColor}\"}} \n" +
                         "}")
            .Build();

        MqttClient.PublishAsync(applicationMessage, CancellationToken.None);
    }
    
    
    public void TurnOff()
    {
        var applicationMessage = new MqttApplicationMessageBuilder()
            .WithTopic($"{RootTopic + Id}/set")
            .WithPayload("{\"state\": \"OFF\"}")
            .Build();

        MqttClient.PublishAsync(applicationMessage, CancellationToken.None);
    }
}