#input format: [[[x,y,w,h],label
import numpy as np

class ObjectMonitor:
    #def __init__(self, img_width, img_height, half_detection_width, half_detection_height,debug_mode=False):
    def __init__(self, img_width, half_detection_width, outlier_percent=0.2, max_alert_range=40000, min_alert_range=200,debug_mode=False):
        """
        Detect close objects from bbox results
        :param img_width: input img width
        :param half_detection_width: half of the detection range from center, only bboxes in this range will be monitored
        :param outlier_percent: percent of data to be removed from both front and end of sorted depth readings
        :param max_alert_range: trigger alert if distance<max alert_range and distance>min_alert_range
        :param min_alert_range:
        """
        self.width_bound = [round(img_width/2 - half_detection_width), round(img_width/2 + half_detection_width)]
        self.outlier_percent=outlier_percent
        self.max_alert_range=max_alert_range
        self.min_alert_range=min_alert_range
        self.debug_mode=debug_mode
        #self.height_bound = [round(img_height/2 - half_detection_height), round(img_height/2 + half_detection_height)]

    def process_bboxes(self, depth_frame, bboxes):
        """
        Process Bounding Boxes
        :param depth_frame: depth frame as numpy matrix
        :param bboxes: a list of lists containing a list of corrdinates [x,y,w,h] and detected label
        :return: a list containing detected label and its distance (feet) from camera. If empty, no objects within range.
            If not empty, it only contains the closest object
        """
        min_dist=np.Inf
        result=[]
        for item in bboxes:
            if item[1] == 'Glasses':
                continue
            print(item)
            print(self.width_bound)
            x,y,w,h = item[0]
            if x>=self.width_bound[0] or x+w <= self.width_bound[1]:
                bbox_depth=depth_frame[y:y+h,x:x+w]
                bbox_depth=np.around(bbox_depth, decimals=-1)
                print(bbox_depth.shape)
                sorted_bbox_depth=np.sort(bbox_depth, axis=None)
                front_bound=round(sorted_bbox_depth.shape[0]*self.outlier_percent)
                end_bound=round(sorted_bbox_depth.shape[0]*(1-self.outlier_percent))
                depth=np.median(sorted_bbox_depth[front_bound:end_bound])
                if depth>self.min_alert_range and depth<self.max_alert_range and depth<min_dist:
                    min_dist=depth
                    result=[item[1],depth]
        if len(result)>0:
            if self.debug_mode:
                print(result[1])
            result[1]=round(0.00328084*result[1], 1)
        return result




