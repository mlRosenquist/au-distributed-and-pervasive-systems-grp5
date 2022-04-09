
using System.Text.Json;
using MQTTnet;
using MQTTnet.Client;
using PillSupervisor.Business.Actuators;
using PillSupervisor.Business.Sensors;

namespace PillSupervisor.ZigBee.PlayGround;

public static class Program
{
    public static class SensorsEnum
    {
        public const string
            LivingRoom_Motion = "Værelse_Motion";
    }
    
    public static class ActuatorsEnum
    {
        public const string
            Kitchen_Light = "Køkken_Lys";
    }
    
    public static TObject DumpToConsole<TObject>(this TObject @object)
    {
        var output = "NULL";
        if (@object != null)
        {
            output = JsonSerializer.Serialize(@object, new JsonSerializerOptions
            {
                WriteIndented = true
            });
        }
        
        Console.WriteLine($"[{@object?.GetType().Name}]:\r\n{output}");
        return @object;
    }
    
    // Main Method
    static async public Task Main(String[] args)
    {
        var mqttFactory = new MqttFactory();
        var sensors = new List<Sensor>();
        var actuators = new List<Actuator>();
        
        using (var mqttClient = mqttFactory.CreateMqttClient())
        {
            // Initialize client
            var mqttClientOptions = new MqttClientOptionsBuilder()
                .WithTcpServer("localhost")
                .Build();
            await mqttClient.ConnectAsync(mqttClientOptions, CancellationToken.None);
            
            // Initialize sensors
            sensors.Add(new IkeaMotion(mqttFactory, mqttClient, "zigbee2mqtt/", "0x680ae2fffef9a940", SensorsEnum.LivingRoom_Motion));
            foreach (var sensor in sensors)
            {
                sensor.InitializeMqtt();
            }
            
            // Initialize actuators
            actuators.Add(new LightStrip(mqttFactory, mqttClient, "zigbee2mqtt/", "0x84fd27fffec8a7fd", ActuatorsEnum.Kitchen_Light));
            foreach (var actuator in actuators)
            {
                //actuator.InitializeMqtt();
            }
            
            // Initialize handler
            mqttClient.ApplicationMessageReceivedAsync += e =>
            {
                // Find the sensor / actuator we received data from
                var sensor = sensors.FirstOrDefault(x => e.ApplicationMessage.Topic.Contains(x.Id));
                var actuator = actuators.FirstOrDefault(x => e.ApplicationMessage.Topic.Contains(x.Id));
                
                // Update the found sensor / actuator
                if (sensor != null)
                    sensor.Update(System.Text.Encoding.UTF8.GetString(e.ApplicationMessage.Payload));
                else if (actuator != null)
                    actuator.Update(System.Text.Encoding.UTF8.GetString(e.ApplicationMessage.Payload));
                else
                {
                    throw new NotImplementedException();
                }
                
                // Evaluate state
                var light = (LightStrip)actuators.First(x => x.Name.Contains(ActuatorsEnum.Kitchen_Light));
                var motion = (IkeaMotion)sensors.First(x => x.Name.Contains(SensorsEnum.LivingRoom_Motion));

                switch (motion.Data.Occupancy)
                {
                    case true:
                        light.TurnOn(100, "#1AEE2E");
                        break;
                    default:
                        light.TurnOn(200, "#EE401A");
                        break;
                }
                
                return Task.CompletedTask;
            };
            
            Console.WriteLine("MQTT client subscribed to topic.");

            Console.WriteLine("Press enter to exit.");
            Console.ReadLine();
        }
    }
}