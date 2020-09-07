import math
import time

EARTH_REDIUS = 6378.137


class Date_Process:
    # 计算经纬度
    @staticmethod
    def getDistance(lat1, lng1, lat2, lng2):
        def rad(self, d):
            return d * math.pi / 180.0

        radLat1 = rad(lat1)
        radLat2 = rad(lat2)
        a = radLat1 - radLat2
        b = rad(lng1) - rad(lng2)
        s = 2 * math.asin(math.sqrt(
            math.pow(math.sin(a / 2), 2) + math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b / 2), 2)))
        s = s * EARTH_REDIUS
        return s * 100

    @staticmethod
    def strftime(timestamp):
        timearry = time.localtime(timestamp)
        datetime = time.strftime('%Y-%m-%d %H:%M:%S', timearry)
        return datetime

    # def Time_gap(self,timestamp1,timestamp2):
