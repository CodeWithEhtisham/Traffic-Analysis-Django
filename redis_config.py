import redis
import json

# Establish a connection to Redis
redis_host = 'localhost'
redis_port = 6379
redis_db = 0
redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

site_key = 'Air Port Road'  # Example site key
redis_client.delete(site_key)  # Delete the existing key if it exists

# for i in range(10, 20):
#     data = {
#         "site_name": "Baleli Road",
#         "frame_number": i,
#         "lane_sides": i,
#         "detection_lines": i,
#         # "frame": base64.b64encode(cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 60])[1]).decode()
#     }
#     obj = json.dumps(data)
#     redis_client(site_key, obj)  # Convert data to JSON string and add it to Redis list

# # frame_data = redis_client.lrange(site_key, 0, -1)
# # for frame in frame_data:
# #     decoded_frame = json.loads(frame.decode())
# #     # convert into dictionary
# #     decoded_frame= dict(decoded_frame)
# #     print(decoded_frame)



# while True:
#     # Use the BLPOP command to retrieve the first frame from the Redis list (blocking until a frame is available)
#     j, frame = redis_client.blpop(site_key)
#     print(j)
#     # Decode and process the frame
#     decoded_frame = json.loads(frame.decode())
#     decoded_frame = dict(decoded_frame)
#     print(decoded_frame)