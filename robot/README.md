# Robot integration — next milestone

The API generates a task object:
{"task_id":"TASK-AB12","target_zone":"E","action":"surface_collection","priority":"HIGH","execution_mode":"assisted_autonomy","status":"READY"}

Next: ESP32 receives the task over Wi-Fi/MQTT, acknowledges it, performs controlled motion/collection, then reports status. Prove command → motion → stop → telemetry before autonomous navigation.
