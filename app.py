from flask import Flask, jsonify, request
import os
import shutil
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.Resize import Resize

app = Flask(__name__)

OUTPUT_FOLDER = 'output'

def convert_mp4_to_gif(input_path, output_path, fps=10, resize=None):
    
    clip = VideoFileClip(input_path)
    if resize:   
        width, height = clip.size
        width=int(width*resize)
        height =int(height *resize)
        print('new size:',(width, height))
        clip=clip.with_effects([Resize((width, height))])
        print('\n\n aaa\n',type(clip))

    # 将视频转换为 GIF
    clip.write_gif(output_path, fps=fps)

    print(f"已保存到: {output_path}")
    return output_path



# 定义一个简单的接口，返回消息
@app.route('/api/message', methods=['GET'])
def get_message():
    print('aaa')
    name = request.args.get('name', 'World')  # 获取参数 name, 默认值为 World
    return jsonify({'message': f'Hello, {name}!'})  # 返回 JSON 格式的消息



def delete_all_files_in_directory(directory):
    # 列出目录中的所有条目（文件、链接和目录）
    for entry in os.listdir(directory):
        path = os.path.join(directory, entry)
        try:
            # 如果是文件或者符号链接，直接删除
            if os.path.isfile(path) or os.path.islink(path):
                os.unlink(path)
            # 如果是目录，则递归删除整个目录
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except Exception as e:
            print(f"删除 {path} 时发生错误: {e}")
            


@app.route('/api/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400

    file = request.files['file']
    print('file：：：',file)
    if file.filename == '':
        return jsonify({"status": "error", "message": "No file selected"}), 400

    # 保存文件到指定目录
    ## - 删除原有的文件
    
    save_path = os.path.join('uploads', file.filename)
    if len(os.listdir())>=1:
    	delete_all_files_in_directory('uploads')
    file.save(save_path)
    print('yes???',save_path)
    input_video=save_path
    gif_filename = os.path.splitext(file.filename)[0] + ".gif"
    output_gif = os.path.join(OUTPUT_FOLDER, gif_filename)
    gif_path=convert_mp4_to_gif(input_video, output_gif, fps=10, resize=0.5)

    return send_file(gif_path, mimetype='image/gif')
    # return jsonify({"status": "success", "message": "File uploaded successfully",'data':save_path}), 200


@app.route('/api/transform', methods=['POST'])
def transform_video():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400
    file = request.files['file']
    input_video=request.files['filepath']
    print('input_video',input_video)
    gif_filename = os.path.splitext(file.filename)[0] + ".gif"
    output_gif = os.path.join(OUTPUT_FOLDER, gif_filename)
    gif_path=convert_mp4_to_gif(input_video, output_gif, fps=10, resize=0.5)
    gif_url = f"http://127.0.0.1:5000/api/download/{gif_filename}"
    return send_file(gif_url, mimetype='image/gif')
    # return jsonify({"status": "success", "message": "File uploaded successfully",'data':save_path}), 200

@app.route('/api/files', methods=['GET'])
def list_files():    
    try:
        files = os.listdir(OUTPUT_FOLDER)
        res={}
        # return jsonify({'files': [f"http://127.0.0.1:5000/api/download/{file}" for file in files]})
        return jsonify({'files': f"http://127.0.0.1:5000/api/download/{files[0]}"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delfile', methods=['GET'])
def delfiles():    
    try:
        # files = os.listdir(OUTPUT_FOLDER)
        delete_all_files_in_directory(OUTPUT_FOLDER)
        # return jsonify({'files': [f"http://127.0.0.1:5000/api/download/{file}" for file in files]})
        return jsonify({"status": "success", "message": "done"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)  # 在 5000 端口运行服务
    
    
# from flask import Flask, request, jsonify, send_file
# #     
# #    
# from flask_cors import CORS
# import os
# from moviepy.video.io.VideoFileClip import VideoFileClip
# from moviepy.video.fx.Resize import Resize

# app = Flask(__name__)
# CORS(app)

# UPLOAD_FOLDER = 'uploads'
# OUTPUT_FOLDER = 'output'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)



# def convert_mp4_to_gif(input_path, output_path, fps=10, resize=None):
    
#     clip = VideoFileClip(input_path)
#     if resize:   
#         width, height = clip.size
#         width=int(width*resize)
#         height =int(height *resize)
#         print('new size:',(width, height))
#         clip=clip.with_effects([Resize((width, height))])
#         print('\n\n aaa\n',type(clip))

#     # 将视频转换为 GIF
#     clip.write_gif(output_path, fps=fps)

#     print(f"已保存到: {output_path}")



# # 处理上传
# @app.route('/api/upload', methods=['POST'])
# def upload_video():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file uploaded'}), 400

#     file = request.files['file']
#     filename = os.path.join(UPLOAD_FOLDER, file.filename)
#     file.save(filename)

#     # 生成 GIF
#     gif_filename = os.path.splitext(file.filename)[0] + ".gif"
#     gif_path = os.path.join(OUTPUT_FOLDER, gif_filename)
#     # convert_video_to_gif(filename, gif_path)
#     convert_mp4_to_gif(filename, gif_path,  fps=10, resize=None)

#     gif_url = f"http://127.0.0.1:5000/api/download/{gif_filename}"
#     return send_file(gif_path, mimetype='image/gif')
#     # return jsonify({'gif_url': gif_url})

# # MP4 转 GIF
# def convert_video_to_gif(video_path, output_gif_path):
#     clip = VideoFileClip(video_path)
#     clip = clip.subclip(0, min(5, clip.duration))  # 取前 5 秒
#     clip = clip.resize(width=480)  # 限制 GIF 尺寸
#     clip.write_gif(output_gif_path, fps=10)

# # 处理 GIF 下载
# @app.route('/api/download/<filename>', methods=['GET'])
# def download_gif(filename):
#     gif_path = os.path.join(OUTPUT_FOLDER, filename)
#     if os.path.exists(gif_path):
#         return send_file(gif_path, mimetype='image/gif')
#     else:
#         return jsonify({'error': 'File not found'}), 404

# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=5000) 

