import asyncio
from winrt.windows.storage.streams import \
    DataReader, Buffer, InputStreamOptions
async def get_media_info():
    info_dict=[]
    result=""

    from winrt.windows.media.control import \
        GlobalSystemMediaTransportControlsSessionManager as MediaManager
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()

    if current_session:  # there needs to be a media session running
       # if current_session.source_app_user_model_id == TARGET_ID:
        info = await current_session.try_get_media_properties_async()

        # song_attr[0] != '_' ignores system attributes
        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

        # converts winrt vector to list
        info_dict['genres'] = list(info_dict['genres'])
        result=info_dict['title']+"-"+info_dict['album_artist']
        #print(info_dict)

    return [info_dict,result]



async def read_stream_into_buffer(stream_ref, buffer):
    readable_stream = await stream_ref.open_read_async()
    readable_stream.read_async(buffer, buffer.capacity, InputStreamOptions.READ_AHEAD)


    # create the current_media_info dict with the earlier code first

    # copies data from data stream reference into buffer created above
def title():
    current_media_info = asyncio.run(get_media_info())[1]
    return current_media_info
def thumb():
    try:
        current_media_info = asyncio.run(get_media_info())[0]
        thumb_stream_ref = current_media_info['thumbnail']

        # 5MB (5 million byte) buffer - thumbnail unlikely to be larger
        thumb_read_buffer = Buffer(5000000)

        asyncio.run(read_stream_into_buffer(thumb_stream_ref, thumb_read_buffer))

        # reads data (as bytes) from buffer
        buffer_reader = DataReader.from_buffer(thumb_read_buffer)
        byte_buffer = buffer_reader.read_bytes(thumb_read_buffer.length)

        with open('C:\zpz\\tmbb.png', 'wb+') as fobj:
            fobj.write(bytearray(byte_buffer))
    except:
        print("thumb 失败")
    #print("thumb")
#print(asyncio.run(get_media_info())[1])
