"""
素材管理
@project: wxopen
@auth: Eric Joe
@email: whatisjava@hotmail.com
@build: 2019/10/10 16:45
@info: 
"""

from wxrequest import WeChatRequest


class MaterialRequest(WeChatRequest):

    def upload_temp_material(self, material_type, material_path):
        """
        新增临时素材
        :param material_type: 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb，主要用于视频与音乐格式的缩略图）
        :param material_path: 图片地址
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s' % (self.access_token, material_type)
        files = {'media': (material_path, open(material_path, 'rb'), 'image/*', {})}
        content = self.requests.post(url, files=files).content.decode('utf8')
        return self.render(content)

    def upload_temp_image_material(self, material_path):
        """
        新增临时素材（图片）: 2M，支持PNG/JPEG/JPG/GIF格式
        :param material_path:
        :return:
        """
        self.validate_suffix(material_path, ('png', 'jpeg', 'jpg', 'gif'))
        return self.upload_temp_material('image', material_path)

    def upload_temp_voice_material(self, material_path):
        """
        新增临时素材（语音）: 2M，播放长度不超过60s，支持AMR/MP3格式
        :param material_path:
        :return:
        """
        self.validate_suffix(material_path, ('amr', 'mp3'))
        return self.upload_temp_material('voice', material_path)

    def upload_temp_video_material(self, material_path):
        """
        新增临时素材（视频）: 10MB，支持MP4格式
        :param material_path:
        :return:
        """
        self.validate_suffix(material_path, ('mp4',))
        return self.upload_temp_material('video', material_path)

    def upload_temp_thumb_material(self, material_path):
        """
        新增临时素材（缩略图）: 64KB，支持JPG格式
        :param material_path:
        :return:
        """
        self.validate_suffix(material_path, ('jpg',))
        return self.upload_temp_material('video', material_path)
