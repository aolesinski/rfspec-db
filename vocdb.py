#!/usr/bin/env python3

'''
@author: Adam Olesiński
'''

from dict2xml import dict2xml
import cv2
import os
import glob

def signals2dict(signals):
    objs = []
    for signal in signals:
        rois = signal.get_rois()
        for roi in rois:
            obj = {
                'name' : signal.name,
                'pose' : signal.pose,
                'truncated' : signal.truncated,
                'difficult' : signal.difficult,
                'bndbox' : roi
                }
            objs.append(obj)
    return objs


class VocDB:

    def __init__(self, db_path, voc_folder='VOC2007', overwrite=True, img_ext='jpg'):
        self.db_path = db_path
        self.db_objects = []
        self.processed_paths = []
        self.check_path(self.db_path)

        self.voc_folder_name = voc_folder
        self.overwrite = overwrite

        self.db_voc_path = self.db_path + '/' + self.voc_folder_name
        self.check_path(self.db_voc_path)

        self.annotation_dir = 'Annotations'
        self.annotation_path = self.db_voc_path + '/' + self.annotation_dir

        self.segmentation_class_dir = 'SegmentationClass'
        self.segmentation_class_path = self.db_voc_path + '/' + self.segmentation_class_dir

        self.segmentation_object_dir = 'SegmentationObjects'
        self.segmentation_object_path = self.db_voc_path + '/' + self.segmentation_object_dir
 
        self.segmentation_debug_dir = 'SegmentationSignalsDebug'
        self.segmentation_debug_path = self.db_voc_path + '/' + self.segmentation_debug_dir
       
        self.image_sets_dir = 'ImageSets'
        self.image_sets_path = self.db_voc_path + '/' + self.image_sets_dir

        self.jpeg_images_dir = 'JPEGImages'
        self.jpeg_images_path =  self.db_voc_path + '/' + self.jpeg_images_dir

        self.helper_images_dir = 'HelperImages'
        self.helper_images_path =  self.db_voc_path + '/' + self.helper_images_dir

        self.noise_images_dir = 'NoiseImages'
        self.noise_images_path =  self.db_voc_path + '/' + self.noise_images_dir

        self.visualisations_dir = 'Visualisations'
        self.visualisations_path =  self.db_voc_path + '/' + self.visualisations_dir

        self.images_file_extension = img_ext
        self.annotations_file_extension = 'xml'
        self.db_object_filename_digits = 6
        self.db_object_iter = 0
        self.db_object_filename = ''

        self.annotation_files = []
        self.segmentation_class_files = []
        self.segmentation_object_files = []
        self.image_sets_files = []
        self.jpeg_images_files = []
        self.helper_images_files = []
        self.noise_images_files = []
        self.visualisations_files = []

    def get_files(self, path, ext):
        files = sorted(glob.glob(os.path.join(path, '*.' + str(ext))))
        return files

    def load(self):
        path = self.annotation_path
        size_list = []
        if self.check_path(path, False, False):
            files = self.get_files(path, self.annotations_file_extension)
            self.annotation_files = files
            size_list.append(len(files))

        path = self.segmentation_class_path
        if self.check_path(path, False, False):
            files = self.get_files(path, self.images_file_extension)
            self.segmentation_class_files = files
            size_list.append(len(files))

        path = self.segmentation_object_path
        if self.check_path(path, False, False):
            files = self.get_files(path, self.images_file_extension)
            self.segmentation_object_files = files
            size_list.append(len(files))

        path = self.image_sets_path
        if self.check_path(path, False, False):
            files = self.get_files(path, self.images_file_extension)
            self.image_sets_files = files
            size_list.append(len(files))

        path = self.jpeg_images_path
        if self.check_path(path, False, False):
            files = self.get_files(path, self.images_file_extension)
            self.jpeg_images_files = files
            size_list.append(len(files))

        path = self.helper_images_path
        if self.check_path(path, False, False):
            files = self.get_files(path, self.images_file_extension)
            self.helper_images_files = files
            size_list.append(len(files))

        path = self.noise_images_path
        if self.check_path(path, False, False):
            files = self.get_files(path, self.images_file_extension)
            self.noise_images_files = files
            size_list.append(len(files))

        path = self.visualisations_path
        if self.check_path(path, False, False):
            files = self.get_files(path, self.images_file_extension)
            self.visualisations_files = files
            size_list.append(len(files))

        result = size_list.count(size_list[0]) == len(size_list)
        if not result:
            print('Difference in number of files')
            return False

        self.db_object_iter = size_list[0]
        return True

    def get_object_iter(self):
        return self.db_object_iter

    def get_db_object(self, db_object, index):
        if index > len(db_object) - 1:
            return []
        else:
            return db_object[index]

    def get(self, index):
        db_dict = {
            'visualisation' : self.get_db_object(self.visualisations_files, index),
            'helper_image' : self.get_db_object(self.helper_images_files, index),
            'noise_image' : self.get_db_object(self.noise_images_files, index),
            'jpeg_image' : self.get_db_object(self.jpeg_images_files, index),
            'segmentation_object' : self.get_db_object(self.segmentation_object_files, index),
            'segmentation_class' : self.get_db_object(self.segmentation_class_files, index),
            'annotation' : self.get_db_object(self.annotation_files, index),
                }
        return db_dict

    def check_path(self, path, overwrite=False, autocreate=True):
        if path in self.processed_paths:
            return True
        if(not os.path.exists(path)):
            if autocreate:
                try:
                    print('path',path,'not exist, creating')
                    os.makedirs(path)
                    self.processed_paths.append(path)
                    return True
                except Exception as e:
                    print(e)
                    return False
            else:
                print('path',path,'not exist')
                return False
        else:
            print('path',path,'exist')
            if overwrite:
                for f in os.listdir(path):
                    os.remove(os.path.join(path, f))
                    self.processed_paths.append(path)
        return True

    def new_db_object(self):
        self.db_object_iter += 1
        self.db_object_filename = str(self.db_object_iter).zfill(self.db_object_filename_digits)
        self.db_objects.append(self.db_object_filename)

    def process_annotation(self, segmented, width, height, depth, objects):
        self.__bool2int(segmented)
        annotation_data = self.__prepare_xml_annotation(segmented=segmented, width=width, height=height, depth=depth, objects=objects)
        return self.__save_annotation(annotation_data)

    def process_image(self, image):
        path = self.jpeg_images_path
        return self.__save_image(image, path)

    def process_helper_image(self, helper_image):
        path = self.helper_images_path
        return self.__save_image(helper_image, path)

    def process_noise_image(self, noise_image):
        path = self.noise_images_path
        return self.__save_image(noise_image, path)

    def process_visualisation(self, image):
        path = self.visualisations_path
        return self.__save_image(image, path)

    def process_segmentation(self, images, debug=False):
        if debug:
            for i in range(len(images)):
                image = images[i]
                path = self.segmentation_debug_path
                file_suffix = '_s' + str(i)
                self.__save_image(image, path, file_suffix)
        else:
            tmp_img = images[0]
            for i in images:
                tmp_img = cv2.add(tmp_img, i)
            path = self.segmentation_object_path
            file_suffix = '' #_s' + str(i)
            self.__save_image(tmp_img, path, file_suffix)

    def __save_image(self, image, path, file_suffix='', file_extension=None):
        if file_extension is None:
            file_extension = self.images_file_extension
        if self.check_path(path, overwrite=self.overwrite):
            pth = path + '/' + self.db_object_filename + file_suffix + '.' + file_extension
            try:
                print('saving image to',pth)
                cv2.imwrite(pth, image)
                return True
            except Exception as e:
                print(e)
                return False
        return False

    def __save_annotation(self, data, file_extension=None):
        if file_extension is None:
            file_extension = self.annotations_file_extension
        if self.check_path(self.annotation_path, overwrite=self.overwrite):
            path = self.annotation_path + '/' + self.db_object_filename + '.' + file_extension
            try:
                print('saving annotation to',path)
                afile = open(path, 'w')
                afile.write(data)
                afile.close()
                return True
            except Exception as e:
                print(e)
                return False
        return False

    def __prepare_xml_annotation(self, segmented, width, height, depth, objects):
        annotation_dict={}
        adict={}
        size_dict = {}
    
        size_dict['width'] = width
        size_dict['height'] = height
        size_dict['depth'] = depth
    
        adict['folder'] = self.voc_folder_name
        adict['filename'] = self.db_object_filename + '.' + self.images_file_extension
        adict['size'] = size_dict
        adict['segmented'] = segmented

        object_iter = 0
        for i in objects:
            object_str = 'object' + str(object_iter)
            adict[object_str] = i
            object_iter += 1
        annotation_dict['annotation'] = adict

        xml = dict2xml(annotation_dict)
        for i in range(object_iter+1):
            obj_str = 'object' + str(i)
            obj_str_start = '<' + obj_str + '>'
            obj_str_stop = '</' + obj_str + '>'
            xml = xml.replace(obj_str_start, '<object>')
            xml = xml.replace(obj_str_stop, '</object>')
        return xml


    def __bool2int(self, data):
        if isinstance(data, bool):
            if data:
                data = 1
            else:
                data = 0
        return int(data)

'''
filename = 'spectrum1.jpg'
segmented = 0
width = 250
height = 250
depth = 3
obj1 = {
        'name' : 'signal',
        'pose' : 'unspecified',
        'truncated' : 0,
        'difficult' : 0,
        'bndbox' : {
            'xmin' : 198,
            'ymin' : 148,
            'xmax' : 261,
            'ymax' : 235
            }
        }
objects = [obj1, obj1, obj1]

vocdb = VocDB('/home/aolesinski/tempvocdb')

vocdb.new_db_object()
status = vocdb.process_annotation(width=width, height=height, depth=depth,
                   segmented=segmented, objects=objects)
print('status:',status)
'''
