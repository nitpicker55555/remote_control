import cv2
class Compress_img:

    def __init__(self, img_path):
        self.img_path = img_path
        self.img_name = img_path.split('/')[-1]

    def compress_img_CV(self, compress_rate=0.5, show=False):
        img = cv2.imread(self.img_path)
        heigh, width = img.shape[:2]
        # 双三次插值
        img_resize = cv2.resize(img, (int(width*compress_rate), int(heigh*compress_rate)),
                                interpolation=cv2.INTER_AREA)
        encode_param = [cv2.IMWRITE_PNG_COMPRESSION, 4]
        cv2.imwrite("result_cv_" + self.img_name, img_resize, encode_param)
        print("%s 已压缩，" % (self.img_name), "压缩率：", compress_rate)
        if show:
            cv2.imshow(self.img_name, img_resize)
            cv2.waitKey(0)

if __name__ == '__main__':
    img_path = "C:/zpz/Figure_1.png"
    compress = Compress_img(img_path)

    # 使用opencv压缩图片
    compress.compress_img_CV()
