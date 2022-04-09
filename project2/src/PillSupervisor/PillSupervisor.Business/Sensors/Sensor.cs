using MQTTnet;
using MQTTnet.Client;

namespace PillSupervisor.Business.Sensors;

public class Sensor
{
    protected MqttFactory MqttFactory;
    protected MqttClient MqttClient;
    public string RootTopic;
    public string Id;
    public string Name;
    protected bool Initialized;
    public Sensor(MqttFactory mqttFactory, MqttClient mqttClient, string rootTopic, string id, string name)
    {
        MqttFactory = mqttFactory;
        MqttClient = mqttClient;
        RootTopic = rootTopic;
        Id = id;
        Name = name;
    }

    public void InitializeMqtt()
    {
        if (Initialized)
            return;
        
        var mqttSubscribeOptions = MqttFactory.CreateSubscribeOptionsBuilder()
            .WithTopicFilter(f => { f.WithTopic($"{RootTopic + Id}"); })
            .Build();
        
        MqttClient.SubscribeAsync(mqttSubscribeOptions, CancellationToken.None);

        Initialized = true;
    }

    public virtual void Update(string payload)
    {
        
    }
}