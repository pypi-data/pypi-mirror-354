# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from typing import List, BinaryIO, Dict, Any


class AnalyzeChestVesselRequestURLList(TeaModel):
    def __init__(
        self,
        url: str = None,
    ):
        # This parameter is required.
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.url is not None:
            result['URL'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.url = m.get('URL')
        return self


class AnalyzeChestVesselRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        data_source_type: str = None,
        org_id: str = None,
        org_name: str = None,
        urllist: List[AnalyzeChestVesselRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.data_source_type = data_source_type
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # 1
        # 
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.data_source_type is not None:
            result['DataSourceType'] = self.data_source_type
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('DataSourceType') is not None:
            self.data_source_type = m.get('DataSourceType')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = AnalyzeChestVesselRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class AnalyzeChestVesselAdvanceRequestURLList(TeaModel):
    def __init__(
        self,
        urlobject: BinaryIO = None,
    ):
        # This parameter is required.
        self.urlobject = urlobject

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.urlobject is not None:
            result['URL'] = self.urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.urlobject = m.get('URL')
        return self


class AnalyzeChestVesselAdvanceRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        data_source_type: str = None,
        org_id: str = None,
        org_name: str = None,
        urllist: List[AnalyzeChestVesselAdvanceRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.data_source_type = data_source_type
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # 1
        # 
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.data_source_type is not None:
            result['DataSourceType'] = self.data_source_type
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('DataSourceType') is not None:
            self.data_source_type = m.get('DataSourceType')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = AnalyzeChestVesselAdvanceRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class AnalyzeChestVesselResponseBodyDataAortaInfo(TeaModel):
    def __init__(
        self,
        area: List[float] = None,
        coordinates: List[List[float]] = None,
        label_value: int = None,
        max_area: float = None,
        max_area_index: int = None,
        max_diameter: float = None,
    ):
        # 1
        self.area = area
        self.coordinates = coordinates
        self.label_value = label_value
        self.max_area = max_area
        self.max_area_index = max_area_index
        self.max_diameter = max_diameter

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.area is not None:
            result['Area'] = self.area
        if self.coordinates is not None:
            result['Coordinates'] = self.coordinates
        if self.label_value is not None:
            result['LabelValue'] = self.label_value
        if self.max_area is not None:
            result['MaxArea'] = self.max_area
        if self.max_area_index is not None:
            result['MaxAreaIndex'] = self.max_area_index
        if self.max_diameter is not None:
            result['MaxDiameter'] = self.max_diameter
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Area') is not None:
            self.area = m.get('Area')
        if m.get('Coordinates') is not None:
            self.coordinates = m.get('Coordinates')
        if m.get('LabelValue') is not None:
            self.label_value = m.get('LabelValue')
        if m.get('MaxArea') is not None:
            self.max_area = m.get('MaxArea')
        if m.get('MaxAreaIndex') is not None:
            self.max_area_index = m.get('MaxAreaIndex')
        if m.get('MaxDiameter') is not None:
            self.max_diameter = m.get('MaxDiameter')
        return self


class AnalyzeChestVesselResponseBodyDataPulmonaryInfo(TeaModel):
    def __init__(
        self,
        area: List[float] = None,
        coordinates: List[List[float]] = None,
        label_value: int = None,
        max_area: float = None,
        max_area_index: int = None,
        max_diameter: float = None,
        nearest_aorta_area: float = None,
    ):
        # 1
        self.area = area
        self.coordinates = coordinates
        self.label_value = label_value
        self.max_area = max_area
        self.max_area_index = max_area_index
        self.max_diameter = max_diameter
        self.nearest_aorta_area = nearest_aorta_area

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.area is not None:
            result['Area'] = self.area
        if self.coordinates is not None:
            result['Coordinates'] = self.coordinates
        if self.label_value is not None:
            result['LabelValue'] = self.label_value
        if self.max_area is not None:
            result['MaxArea'] = self.max_area
        if self.max_area_index is not None:
            result['MaxAreaIndex'] = self.max_area_index
        if self.max_diameter is not None:
            result['MaxDiameter'] = self.max_diameter
        if self.nearest_aorta_area is not None:
            result['NearestAortaArea'] = self.nearest_aorta_area
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Area') is not None:
            self.area = m.get('Area')
        if m.get('Coordinates') is not None:
            self.coordinates = m.get('Coordinates')
        if m.get('LabelValue') is not None:
            self.label_value = m.get('LabelValue')
        if m.get('MaxArea') is not None:
            self.max_area = m.get('MaxArea')
        if m.get('MaxAreaIndex') is not None:
            self.max_area_index = m.get('MaxAreaIndex')
        if m.get('MaxDiameter') is not None:
            self.max_diameter = m.get('MaxDiameter')
        if m.get('NearestAortaArea') is not None:
            self.nearest_aorta_area = m.get('NearestAortaArea')
        return self


class AnalyzeChestVesselResponseBodyData(TeaModel):
    def __init__(
        self,
        aorta_info: AnalyzeChestVesselResponseBodyDataAortaInfo = None,
        pulmonary_info: AnalyzeChestVesselResponseBodyDataPulmonaryInfo = None,
        result_url: str = None,
    ):
        self.aorta_info = aorta_info
        self.pulmonary_info = pulmonary_info
        self.result_url = result_url

    def validate(self):
        if self.aorta_info:
            self.aorta_info.validate()
        if self.pulmonary_info:
            self.pulmonary_info.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.aorta_info is not None:
            result['AortaInfo'] = self.aorta_info.to_map()
        if self.pulmonary_info is not None:
            result['PulmonaryInfo'] = self.pulmonary_info.to_map()
        if self.result_url is not None:
            result['ResultURL'] = self.result_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AortaInfo') is not None:
            temp_model = AnalyzeChestVesselResponseBodyDataAortaInfo()
            self.aorta_info = temp_model.from_map(m['AortaInfo'])
        if m.get('PulmonaryInfo') is not None:
            temp_model = AnalyzeChestVesselResponseBodyDataPulmonaryInfo()
            self.pulmonary_info = temp_model.from_map(m['PulmonaryInfo'])
        if m.get('ResultURL') is not None:
            self.result_url = m.get('ResultURL')
        return self


class AnalyzeChestVesselResponseBody(TeaModel):
    def __init__(
        self,
        data: AnalyzeChestVesselResponseBodyData = None,
        message: str = None,
        request_id: str = None,
    ):
        self.data = data
        self.message = message
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = AnalyzeChestVesselResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class AnalyzeChestVesselResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: AnalyzeChestVesselResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = AnalyzeChestVesselResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CalcBMDRequestURLList(TeaModel):
    def __init__(
        self,
        url: str = None,
    ):
        # This parameter is required.
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.url is not None:
            result['URL'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.url = m.get('URL')
        return self


class CalcBMDRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        org_id: str = None,
        org_name: str = None,
        source_type: str = None,
        urllist: List[CalcBMDRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.source_type = source_type
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        if self.source_type is not None:
            result['SourceType'] = self.source_type
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        if m.get('SourceType') is not None:
            self.source_type = m.get('SourceType')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = CalcBMDRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class CalcBMDAdvanceRequestURLList(TeaModel):
    def __init__(
        self,
        urlobject: BinaryIO = None,
    ):
        # This parameter is required.
        self.urlobject = urlobject

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.urlobject is not None:
            result['URL'] = self.urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.urlobject = m.get('URL')
        return self


class CalcBMDAdvanceRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        org_id: str = None,
        org_name: str = None,
        source_type: str = None,
        urllist: List[CalcBMDAdvanceRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.source_type = source_type
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        if self.source_type is not None:
            result['SourceType'] = self.source_type
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        if m.get('SourceType') is not None:
            self.source_type = m.get('SourceType')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = CalcBMDAdvanceRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class CalcBMDResponseBodyDataDetections(TeaModel):
    def __init__(
        self,
        vert_bmd: float = None,
        vert_category: float = None,
        vert_id: str = None,
        vert_tscore: float = None,
        vert_zscore: float = None,
    ):
        self.vert_bmd = vert_bmd
        self.vert_category = vert_category
        self.vert_id = vert_id
        self.vert_tscore = vert_tscore
        self.vert_zscore = vert_zscore

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.vert_bmd is not None:
            result['VertBMD'] = self.vert_bmd
        if self.vert_category is not None:
            result['VertCategory'] = self.vert_category
        if self.vert_id is not None:
            result['VertId'] = self.vert_id
        if self.vert_tscore is not None:
            result['VertTScore'] = self.vert_tscore
        if self.vert_zscore is not None:
            result['VertZScore'] = self.vert_zscore
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('VertBMD') is not None:
            self.vert_bmd = m.get('VertBMD')
        if m.get('VertCategory') is not None:
            self.vert_category = m.get('VertCategory')
        if m.get('VertId') is not None:
            self.vert_id = m.get('VertId')
        if m.get('VertTScore') is not None:
            self.vert_tscore = m.get('VertTScore')
        if m.get('VertZScore') is not None:
            self.vert_zscore = m.get('VertZScore')
        return self


class CalcBMDResponseBodyData(TeaModel):
    def __init__(
        self,
        detections: List[CalcBMDResponseBodyDataDetections] = None,
        origin: List[float] = None,
        result_url: str = None,
        spacing: List[float] = None,
    ):
        self.detections = detections
        self.origin = origin
        self.result_url = result_url
        self.spacing = spacing

    def validate(self):
        if self.detections:
            for k in self.detections:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Detections'] = []
        if self.detections is not None:
            for k in self.detections:
                result['Detections'].append(k.to_map() if k else None)
        if self.origin is not None:
            result['Origin'] = self.origin
        if self.result_url is not None:
            result['ResultURL'] = self.result_url
        if self.spacing is not None:
            result['Spacing'] = self.spacing
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.detections = []
        if m.get('Detections') is not None:
            for k in m.get('Detections'):
                temp_model = CalcBMDResponseBodyDataDetections()
                self.detections.append(temp_model.from_map(k))
        if m.get('Origin') is not None:
            self.origin = m.get('Origin')
        if m.get('ResultURL') is not None:
            self.result_url = m.get('ResultURL')
        if m.get('Spacing') is not None:
            self.spacing = m.get('Spacing')
        return self


class CalcBMDResponseBody(TeaModel):
    def __init__(
        self,
        data: CalcBMDResponseBodyData = None,
        message: str = None,
        request_id: str = None,
    ):
        self.data = data
        self.message = message
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = CalcBMDResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class CalcBMDResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CalcBMDResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CalcBMDResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CalcCACSRequestURLList(TeaModel):
    def __init__(
        self,
        url: str = None,
    ):
        # This parameter is required.
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.url is not None:
            result['URL'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.url = m.get('URL')
        return self


class CalcCACSRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        data_source_type: str = None,
        org_id: str = None,
        org_name: str = None,
        urllist: List[CalcCACSRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.data_source_type = data_source_type
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.data_source_type is not None:
            result['DataSourceType'] = self.data_source_type
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('DataSourceType') is not None:
            self.data_source_type = m.get('DataSourceType')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = CalcCACSRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class CalcCACSAdvanceRequestURLList(TeaModel):
    def __init__(
        self,
        urlobject: BinaryIO = None,
    ):
        # This parameter is required.
        self.urlobject = urlobject

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.urlobject is not None:
            result['URL'] = self.urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.urlobject = m.get('URL')
        return self


class CalcCACSAdvanceRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        data_source_type: str = None,
        org_id: str = None,
        org_name: str = None,
        urllist: List[CalcCACSAdvanceRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.data_source_type = data_source_type
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.data_source_type is not None:
            result['DataSourceType'] = self.data_source_type
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('DataSourceType') is not None:
            self.data_source_type = m.get('DataSourceType')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = CalcCACSAdvanceRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class CalcCACSResponseBodyDataDetections(TeaModel):
    def __init__(
        self,
        calcium_center: List[int] = None,
        calcium_id: int = None,
        calcium_score: float = None,
        calcium_volume: float = None,
    ):
        self.calcium_center = calcium_center
        self.calcium_id = calcium_id
        self.calcium_score = calcium_score
        self.calcium_volume = calcium_volume

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.calcium_center is not None:
            result['CalciumCenter'] = self.calcium_center
        if self.calcium_id is not None:
            result['CalciumId'] = self.calcium_id
        if self.calcium_score is not None:
            result['CalciumScore'] = self.calcium_score
        if self.calcium_volume is not None:
            result['CalciumVolume'] = self.calcium_volume
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CalciumCenter') is not None:
            self.calcium_center = m.get('CalciumCenter')
        if m.get('CalciumId') is not None:
            self.calcium_id = m.get('CalciumId')
        if m.get('CalciumScore') is not None:
            self.calcium_score = m.get('CalciumScore')
        if m.get('CalciumVolume') is not None:
            self.calcium_volume = m.get('CalciumVolume')
        return self


class CalcCACSResponseBodyData(TeaModel):
    def __init__(
        self,
        detections: List[CalcCACSResponseBodyDataDetections] = None,
        result_url: str = None,
        score: str = None,
        volume_score: str = None,
    ):
        self.detections = detections
        self.result_url = result_url
        self.score = score
        self.volume_score = volume_score

    def validate(self):
        if self.detections:
            for k in self.detections:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Detections'] = []
        if self.detections is not None:
            for k in self.detections:
                result['Detections'].append(k.to_map() if k else None)
        if self.result_url is not None:
            result['ResultUrl'] = self.result_url
        if self.score is not None:
            result['Score'] = self.score
        if self.volume_score is not None:
            result['VolumeScore'] = self.volume_score
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.detections = []
        if m.get('Detections') is not None:
            for k in m.get('Detections'):
                temp_model = CalcCACSResponseBodyDataDetections()
                self.detections.append(temp_model.from_map(k))
        if m.get('ResultUrl') is not None:
            self.result_url = m.get('ResultUrl')
        if m.get('Score') is not None:
            self.score = m.get('Score')
        if m.get('VolumeScore') is not None:
            self.volume_score = m.get('VolumeScore')
        return self


class CalcCACSResponseBody(TeaModel):
    def __init__(
        self,
        data: CalcCACSResponseBodyData = None,
        message: str = None,
        request_id: str = None,
    ):
        self.data = data
        self.message = message
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = CalcCACSResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class CalcCACSResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: CalcCACSResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = CalcCACSResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DetectCovid19CadRequestURLList(TeaModel):
    def __init__(
        self,
        url: str = None,
    ):
        # This parameter is required.
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.url is not None:
            result['URL'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.url = m.get('URL')
        return self


class DetectCovid19CadRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        org_id: str = None,
        org_name: str = None,
        urllist: List[DetectCovid19CadRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = DetectCovid19CadRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class DetectCovid19CadAdvanceRequestURLList(TeaModel):
    def __init__(
        self,
        urlobject: BinaryIO = None,
    ):
        # This parameter is required.
        self.urlobject = urlobject

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.urlobject is not None:
            result['URL'] = self.urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.urlobject = m.get('URL')
        return self


class DetectCovid19CadAdvanceRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        org_id: str = None,
        org_name: str = None,
        urllist: List[DetectCovid19CadAdvanceRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = DetectCovid19CadAdvanceRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class DetectCovid19CadResponseBodyData(TeaModel):
    def __init__(
        self,
        lesion_ratio: str = None,
        mask: str = None,
        new_probability: str = None,
        normal_probability: str = None,
        other_probability: str = None,
    ):
        self.lesion_ratio = lesion_ratio
        self.mask = mask
        self.new_probability = new_probability
        self.normal_probability = normal_probability
        self.other_probability = other_probability

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lesion_ratio is not None:
            result['LesionRatio'] = self.lesion_ratio
        if self.mask is not None:
            result['Mask'] = self.mask
        if self.new_probability is not None:
            result['NewProbability'] = self.new_probability
        if self.normal_probability is not None:
            result['NormalProbability'] = self.normal_probability
        if self.other_probability is not None:
            result['OtherProbability'] = self.other_probability
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LesionRatio') is not None:
            self.lesion_ratio = m.get('LesionRatio')
        if m.get('Mask') is not None:
            self.mask = m.get('Mask')
        if m.get('NewProbability') is not None:
            self.new_probability = m.get('NewProbability')
        if m.get('NormalProbability') is not None:
            self.normal_probability = m.get('NormalProbability')
        if m.get('OtherProbability') is not None:
            self.other_probability = m.get('OtherProbability')
        return self


class DetectCovid19CadResponseBody(TeaModel):
    def __init__(
        self,
        data: DetectCovid19CadResponseBodyData = None,
        message: str = None,
        request_id: str = None,
    ):
        self.data = data
        self.message = message
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = DetectCovid19CadResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DetectCovid19CadResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DetectCovid19CadResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DetectCovid19CadResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DetectLiverSteatosisRequestURLList(TeaModel):
    def __init__(
        self,
        url: str = None,
    ):
        # This parameter is required.
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.url is not None:
            result['URL'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.url = m.get('URL')
        return self


class DetectLiverSteatosisRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        org_id: str = None,
        org_name: str = None,
        source_type: str = None,
        urllist: List[DetectLiverSteatosisRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.source_type = source_type
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        if self.source_type is not None:
            result['SourceType'] = self.source_type
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        if m.get('SourceType') is not None:
            self.source_type = m.get('SourceType')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = DetectLiverSteatosisRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class DetectLiverSteatosisAdvanceRequestURLList(TeaModel):
    def __init__(
        self,
        urlobject: BinaryIO = None,
    ):
        # This parameter is required.
        self.urlobject = urlobject

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.urlobject is not None:
            result['URL'] = self.urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.urlobject = m.get('URL')
        return self


class DetectLiverSteatosisAdvanceRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        org_id: str = None,
        org_name: str = None,
        source_type: str = None,
        urllist: List[DetectLiverSteatosisAdvanceRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.source_type = source_type
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        if self.source_type is not None:
            result['SourceType'] = self.source_type
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        if m.get('SourceType') is not None:
            self.source_type = m.get('SourceType')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = DetectLiverSteatosisAdvanceRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class DetectLiverSteatosisResponseBodyDataDetections(TeaModel):
    def __init__(
        self,
        fat_fract: float = None,
        liver_hu: float = None,
        liver_roi1: float = None,
        liver_roi2: float = None,
        liver_roi3: float = None,
        liver_slice: float = None,
        liver_spleen_difference: float = None,
        liver_spleen_ratio: float = None,
        liver_volume: float = None,
        maoss_score: float = None,
        prediction: str = None,
        probability: float = None,
        roi1center: List[int] = None,
        roi2center: List[int] = None,
        roi3center: List[int] = None,
        radius: int = None,
        spleen_center: List[int] = None,
        spleen_hu: float = None,
        spleen_roi: float = None,
        spleen_slice: float = None,
        spleen_volume: float = None,
    ):
        self.fat_fract = fat_fract
        self.liver_hu = liver_hu
        self.liver_roi1 = liver_roi1
        self.liver_roi2 = liver_roi2
        self.liver_roi3 = liver_roi3
        self.liver_slice = liver_slice
        self.liver_spleen_difference = liver_spleen_difference
        self.liver_spleen_ratio = liver_spleen_ratio
        self.liver_volume = liver_volume
        self.maoss_score = maoss_score
        self.prediction = prediction
        self.probability = probability
        self.roi1center = roi1center
        self.roi2center = roi2center
        self.roi3center = roi3center
        self.radius = radius
        self.spleen_center = spleen_center
        self.spleen_hu = spleen_hu
        self.spleen_roi = spleen_roi
        self.spleen_slice = spleen_slice
        self.spleen_volume = spleen_volume

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.fat_fract is not None:
            result['FatFract'] = self.fat_fract
        if self.liver_hu is not None:
            result['LiverHU'] = self.liver_hu
        if self.liver_roi1 is not None:
            result['LiverROI1'] = self.liver_roi1
        if self.liver_roi2 is not None:
            result['LiverROI2'] = self.liver_roi2
        if self.liver_roi3 is not None:
            result['LiverROI3'] = self.liver_roi3
        if self.liver_slice is not None:
            result['LiverSlice'] = self.liver_slice
        if self.liver_spleen_difference is not None:
            result['LiverSpleenDifference'] = self.liver_spleen_difference
        if self.liver_spleen_ratio is not None:
            result['LiverSpleenRatio'] = self.liver_spleen_ratio
        if self.liver_volume is not None:
            result['LiverVolume'] = self.liver_volume
        if self.maoss_score is not None:
            result['MaossScore'] = self.maoss_score
        if self.prediction is not None:
            result['Prediction'] = self.prediction
        if self.probability is not None:
            result['Probability'] = self.probability
        if self.roi1center is not None:
            result['ROI1Center'] = self.roi1center
        if self.roi2center is not None:
            result['ROI2Center'] = self.roi2center
        if self.roi3center is not None:
            result['ROI3Center'] = self.roi3center
        if self.radius is not None:
            result['Radius'] = self.radius
        if self.spleen_center is not None:
            result['SpleenCenter'] = self.spleen_center
        if self.spleen_hu is not None:
            result['SpleenHU'] = self.spleen_hu
        if self.spleen_roi is not None:
            result['SpleenROI'] = self.spleen_roi
        if self.spleen_slice is not None:
            result['SpleenSlice'] = self.spleen_slice
        if self.spleen_volume is not None:
            result['SpleenVolume'] = self.spleen_volume
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FatFract') is not None:
            self.fat_fract = m.get('FatFract')
        if m.get('LiverHU') is not None:
            self.liver_hu = m.get('LiverHU')
        if m.get('LiverROI1') is not None:
            self.liver_roi1 = m.get('LiverROI1')
        if m.get('LiverROI2') is not None:
            self.liver_roi2 = m.get('LiverROI2')
        if m.get('LiverROI3') is not None:
            self.liver_roi3 = m.get('LiverROI3')
        if m.get('LiverSlice') is not None:
            self.liver_slice = m.get('LiverSlice')
        if m.get('LiverSpleenDifference') is not None:
            self.liver_spleen_difference = m.get('LiverSpleenDifference')
        if m.get('LiverSpleenRatio') is not None:
            self.liver_spleen_ratio = m.get('LiverSpleenRatio')
        if m.get('LiverVolume') is not None:
            self.liver_volume = m.get('LiverVolume')
        if m.get('MaossScore') is not None:
            self.maoss_score = m.get('MaossScore')
        if m.get('Prediction') is not None:
            self.prediction = m.get('Prediction')
        if m.get('Probability') is not None:
            self.probability = m.get('Probability')
        if m.get('ROI1Center') is not None:
            self.roi1center = m.get('ROI1Center')
        if m.get('ROI2Center') is not None:
            self.roi2center = m.get('ROI2Center')
        if m.get('ROI3Center') is not None:
            self.roi3center = m.get('ROI3Center')
        if m.get('Radius') is not None:
            self.radius = m.get('Radius')
        if m.get('SpleenCenter') is not None:
            self.spleen_center = m.get('SpleenCenter')
        if m.get('SpleenHU') is not None:
            self.spleen_hu = m.get('SpleenHU')
        if m.get('SpleenROI') is not None:
            self.spleen_roi = m.get('SpleenROI')
        if m.get('SpleenSlice') is not None:
            self.spleen_slice = m.get('SpleenSlice')
        if m.get('SpleenVolume') is not None:
            self.spleen_volume = m.get('SpleenVolume')
        return self


class DetectLiverSteatosisResponseBodyData(TeaModel):
    def __init__(
        self,
        detections: List[DetectLiverSteatosisResponseBodyDataDetections] = None,
        origin: List[float] = None,
        result_url: str = None,
        spacing: List[float] = None,
    ):
        self.detections = detections
        self.origin = origin
        self.result_url = result_url
        self.spacing = spacing

    def validate(self):
        if self.detections:
            for k in self.detections:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Detections'] = []
        if self.detections is not None:
            for k in self.detections:
                result['Detections'].append(k.to_map() if k else None)
        if self.origin is not None:
            result['Origin'] = self.origin
        if self.result_url is not None:
            result['ResultUrl'] = self.result_url
        if self.spacing is not None:
            result['Spacing'] = self.spacing
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.detections = []
        if m.get('Detections') is not None:
            for k in m.get('Detections'):
                temp_model = DetectLiverSteatosisResponseBodyDataDetections()
                self.detections.append(temp_model.from_map(k))
        if m.get('Origin') is not None:
            self.origin = m.get('Origin')
        if m.get('ResultUrl') is not None:
            self.result_url = m.get('ResultUrl')
        if m.get('Spacing') is not None:
            self.spacing = m.get('Spacing')
        return self


class DetectLiverSteatosisResponseBody(TeaModel):
    def __init__(
        self,
        data: DetectLiverSteatosisResponseBodyData = None,
        message: str = None,
        request_id: str = None,
    ):
        self.data = data
        self.message = message
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = DetectLiverSteatosisResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DetectLiverSteatosisResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DetectLiverSteatosisResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DetectLiverSteatosisResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DetectLungNoduleRequestURLList(TeaModel):
    def __init__(
        self,
        url: str = None,
    ):
        # This parameter is required.
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.url is not None:
            result['URL'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.url = m.get('URL')
        return self


class DetectLungNoduleRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        org_id: str = None,
        org_name: str = None,
        threshold: float = None,
        urllist: List[DetectLungNoduleRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        self.threshold = threshold
        # 1
        # 
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = DetectLungNoduleRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class DetectLungNoduleAdvanceRequestURLList(TeaModel):
    def __init__(
        self,
        urlobject: BinaryIO = None,
    ):
        # This parameter is required.
        self.urlobject = urlobject

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.urlobject is not None:
            result['URL'] = self.urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.urlobject = m.get('URL')
        return self


class DetectLungNoduleAdvanceRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        org_id: str = None,
        org_name: str = None,
        threshold: float = None,
        urllist: List[DetectLungNoduleAdvanceRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        self.threshold = threshold
        # 1
        # 
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = DetectLungNoduleAdvanceRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class DetectLungNoduleResponseBodyDataSeriesElements(TeaModel):
    def __init__(
        self,
        category: str = None,
        confidence: float = None,
        diameter: float = None,
        image_x: float = None,
        image_y: float = None,
        image_z: float = None,
        lobe: str = None,
        lung: str = None,
        major_axis: List[float] = None,
        mean_value: float = None,
        minor_axis: List[float] = None,
        recist_sopinstance_uid: str = None,
        risk: float = None,
        sopinstance_uid: str = None,
        volume: float = None,
        x: float = None,
        y: float = None,
        z: float = None,
    ):
        self.category = category
        self.confidence = confidence
        self.diameter = diameter
        self.image_x = image_x
        self.image_y = image_y
        self.image_z = image_z
        self.lobe = lobe
        self.lung = lung
        self.major_axis = major_axis
        self.mean_value = mean_value
        self.minor_axis = minor_axis
        # 结节最大径位置所在帧的ID标识。
        self.recist_sopinstance_uid = recist_sopinstance_uid
        # 结节为恶性的置信度。取值范围0~1。
        self.risk = risk
        self.sopinstance_uid = sopinstance_uid
        self.volume = volume
        self.x = x
        self.y = y
        self.z = z

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.category is not None:
            result['Category'] = self.category
        if self.confidence is not None:
            result['Confidence'] = self.confidence
        if self.diameter is not None:
            result['Diameter'] = self.diameter
        if self.image_x is not None:
            result['ImageX'] = self.image_x
        if self.image_y is not None:
            result['ImageY'] = self.image_y
        if self.image_z is not None:
            result['ImageZ'] = self.image_z
        if self.lobe is not None:
            result['Lobe'] = self.lobe
        if self.lung is not None:
            result['Lung'] = self.lung
        if self.major_axis is not None:
            result['MajorAxis'] = self.major_axis
        if self.mean_value is not None:
            result['MeanValue'] = self.mean_value
        if self.minor_axis is not None:
            result['MinorAxis'] = self.minor_axis
        if self.recist_sopinstance_uid is not None:
            result['RecistSOPInstanceUID'] = self.recist_sopinstance_uid
        if self.risk is not None:
            result['Risk'] = self.risk
        if self.sopinstance_uid is not None:
            result['SOPInstanceUID'] = self.sopinstance_uid
        if self.volume is not None:
            result['Volume'] = self.volume
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.z is not None:
            result['Z'] = self.z
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Category') is not None:
            self.category = m.get('Category')
        if m.get('Confidence') is not None:
            self.confidence = m.get('Confidence')
        if m.get('Diameter') is not None:
            self.diameter = m.get('Diameter')
        if m.get('ImageX') is not None:
            self.image_x = m.get('ImageX')
        if m.get('ImageY') is not None:
            self.image_y = m.get('ImageY')
        if m.get('ImageZ') is not None:
            self.image_z = m.get('ImageZ')
        if m.get('Lobe') is not None:
            self.lobe = m.get('Lobe')
        if m.get('Lung') is not None:
            self.lung = m.get('Lung')
        if m.get('MajorAxis') is not None:
            self.major_axis = m.get('MajorAxis')
        if m.get('MeanValue') is not None:
            self.mean_value = m.get('MeanValue')
        if m.get('MinorAxis') is not None:
            self.minor_axis = m.get('MinorAxis')
        if m.get('RecistSOPInstanceUID') is not None:
            self.recist_sopinstance_uid = m.get('RecistSOPInstanceUID')
        if m.get('Risk') is not None:
            self.risk = m.get('Risk')
        if m.get('SOPInstanceUID') is not None:
            self.sopinstance_uid = m.get('SOPInstanceUID')
        if m.get('Volume') is not None:
            self.volume = m.get('Volume')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('Z') is not None:
            self.z = m.get('Z')
        return self


class DetectLungNoduleResponseBodyDataSeries(TeaModel):
    def __init__(
        self,
        elements: List[DetectLungNoduleResponseBodyDataSeriesElements] = None,
        origin: List[float] = None,
        report: str = None,
        series_instance_uid: str = None,
        spacing: List[float] = None,
    ):
        self.elements = elements
        # 1
        self.origin = origin
        self.report = report
        self.series_instance_uid = series_instance_uid
        # 1
        self.spacing = spacing

    def validate(self):
        if self.elements:
            for k in self.elements:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Elements'] = []
        if self.elements is not None:
            for k in self.elements:
                result['Elements'].append(k.to_map() if k else None)
        if self.origin is not None:
            result['Origin'] = self.origin
        if self.report is not None:
            result['Report'] = self.report
        if self.series_instance_uid is not None:
            result['SeriesInstanceUid'] = self.series_instance_uid
        if self.spacing is not None:
            result['Spacing'] = self.spacing
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.elements = []
        if m.get('Elements') is not None:
            for k in m.get('Elements'):
                temp_model = DetectLungNoduleResponseBodyDataSeriesElements()
                self.elements.append(temp_model.from_map(k))
        if m.get('Origin') is not None:
            self.origin = m.get('Origin')
        if m.get('Report') is not None:
            self.report = m.get('Report')
        if m.get('SeriesInstanceUid') is not None:
            self.series_instance_uid = m.get('SeriesInstanceUid')
        if m.get('Spacing') is not None:
            self.spacing = m.get('Spacing')
        return self


class DetectLungNoduleResponseBodyData(TeaModel):
    def __init__(
        self,
        series: List[DetectLungNoduleResponseBodyDataSeries] = None,
    ):
        self.series = series

    def validate(self):
        if self.series:
            for k in self.series:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Series'] = []
        if self.series is not None:
            for k in self.series:
                result['Series'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.series = []
        if m.get('Series') is not None:
            for k in m.get('Series'):
                temp_model = DetectLungNoduleResponseBodyDataSeries()
                self.series.append(temp_model.from_map(k))
        return self


class DetectLungNoduleResponseBody(TeaModel):
    def __init__(
        self,
        data: DetectLungNoduleResponseBodyData = None,
        message: str = None,
        request_id: str = None,
    ):
        self.data = data
        self.message = message
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = DetectLungNoduleResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DetectLungNoduleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DetectLungNoduleResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DetectLungNoduleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DetectLymphRequestURLList(TeaModel):
    def __init__(
        self,
        url: str = None,
    ):
        # This parameter is required.
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.url is not None:
            result['URL'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.url = m.get('URL')
        return self


class DetectLymphRequest(TeaModel):
    def __init__(
        self,
        data_source_type: str = None,
        urllist: List[DetectLymphRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_source_type = data_source_type
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_source_type is not None:
            result['DataSourceType'] = self.data_source_type
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataSourceType') is not None:
            self.data_source_type = m.get('DataSourceType')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = DetectLymphRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class DetectLymphAdvanceRequestURLList(TeaModel):
    def __init__(
        self,
        urlobject: BinaryIO = None,
    ):
        # This parameter is required.
        self.urlobject = urlobject

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.urlobject is not None:
            result['URL'] = self.urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.urlobject = m.get('URL')
        return self


class DetectLymphAdvanceRequest(TeaModel):
    def __init__(
        self,
        data_source_type: str = None,
        urllist: List[DetectLymphAdvanceRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_source_type = data_source_type
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_source_type is not None:
            result['DataSourceType'] = self.data_source_type
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataSourceType') is not None:
            self.data_source_type = m.get('DataSourceType')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = DetectLymphAdvanceRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class DetectLymphResponseBodyDataLesions(TeaModel):
    def __init__(
        self,
        boxes: List[float] = None,
        diametermm: List[float] = None,
        key_slice: int = None,
        recist: List[List[float]] = None,
        score: float = None,
    ):
        self.boxes = boxes
        self.diametermm = diametermm
        self.key_slice = key_slice
        self.recist = recist
        self.score = score

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.boxes is not None:
            result['Boxes'] = self.boxes
        if self.diametermm is not None:
            result['Diametermm'] = self.diametermm
        if self.key_slice is not None:
            result['KeySlice'] = self.key_slice
        if self.recist is not None:
            result['Recist'] = self.recist
        if self.score is not None:
            result['Score'] = self.score
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Boxes') is not None:
            self.boxes = m.get('Boxes')
        if m.get('Diametermm') is not None:
            self.diametermm = m.get('Diametermm')
        if m.get('KeySlice') is not None:
            self.key_slice = m.get('KeySlice')
        if m.get('Recist') is not None:
            self.recist = m.get('Recist')
        if m.get('Score') is not None:
            self.score = m.get('Score')
        return self


class DetectLymphResponseBodyData(TeaModel):
    def __init__(
        self,
        lesions: List[DetectLymphResponseBodyDataLesions] = None,
    ):
        self.lesions = lesions

    def validate(self):
        if self.lesions:
            for k in self.lesions:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Lesions'] = []
        if self.lesions is not None:
            for k in self.lesions:
                result['Lesions'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.lesions = []
        if m.get('Lesions') is not None:
            for k in m.get('Lesions'):
                temp_model = DetectLymphResponseBodyDataLesions()
                self.lesions.append(temp_model.from_map(k))
        return self


class DetectLymphResponseBody(TeaModel):
    def __init__(
        self,
        data: DetectLymphResponseBodyData = None,
        message: str = None,
        request_id: str = None,
    ):
        self.data = data
        # 提交异步任务后的提示信息。
        self.message = message
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = DetectLymphResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DetectLymphResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DetectLymphResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DetectLymphResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DetectPancRequestURLList(TeaModel):
    def __init__(
        self,
        url: str = None,
    ):
        # This parameter is required.
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.url is not None:
            result['URL'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.url = m.get('URL')
        return self


class DetectPancRequest(TeaModel):
    def __init__(
        self,
        data_source_type: str = None,
        urllist: List[DetectPancRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_source_type = data_source_type
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_source_type is not None:
            result['DataSourceType'] = self.data_source_type
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataSourceType') is not None:
            self.data_source_type = m.get('DataSourceType')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = DetectPancRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class DetectPancAdvanceRequestURLList(TeaModel):
    def __init__(
        self,
        urlobject: BinaryIO = None,
    ):
        # This parameter is required.
        self.urlobject = urlobject

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.urlobject is not None:
            result['URL'] = self.urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.urlobject = m.get('URL')
        return self


class DetectPancAdvanceRequest(TeaModel):
    def __init__(
        self,
        data_source_type: str = None,
        urllist: List[DetectPancAdvanceRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_source_type = data_source_type
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_source_type is not None:
            result['DataSourceType'] = self.data_source_type
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataSourceType') is not None:
            self.data_source_type = m.get('DataSourceType')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = DetectPancAdvanceRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class DetectPancResponseBodyDataLesion(TeaModel):
    def __init__(
        self,
        mask: str = None,
        non_pdac_vol: str = None,
        panc_vol: str = None,
        pdac_vol: str = None,
        possibilities: List[str] = None,
    ):
        self.mask = mask
        self.non_pdac_vol = non_pdac_vol
        self.panc_vol = panc_vol
        self.pdac_vol = pdac_vol
        self.possibilities = possibilities

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.mask is not None:
            result['Mask'] = self.mask
        if self.non_pdac_vol is not None:
            result['NonPdacVol'] = self.non_pdac_vol
        if self.panc_vol is not None:
            result['PancVol'] = self.panc_vol
        if self.pdac_vol is not None:
            result['PdacVol'] = self.pdac_vol
        if self.possibilities is not None:
            result['Possibilities'] = self.possibilities
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Mask') is not None:
            self.mask = m.get('Mask')
        if m.get('NonPdacVol') is not None:
            self.non_pdac_vol = m.get('NonPdacVol')
        if m.get('PancVol') is not None:
            self.panc_vol = m.get('PancVol')
        if m.get('PdacVol') is not None:
            self.pdac_vol = m.get('PdacVol')
        if m.get('Possibilities') is not None:
            self.possibilities = m.get('Possibilities')
        return self


class DetectPancResponseBodyData(TeaModel):
    def __init__(
        self,
        lesion: DetectPancResponseBodyDataLesion = None,
    ):
        self.lesion = lesion

    def validate(self):
        if self.lesion:
            self.lesion.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lesion is not None:
            result['Lesion'] = self.lesion.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lesion') is not None:
            temp_model = DetectPancResponseBodyDataLesion()
            self.lesion = temp_model.from_map(m['Lesion'])
        return self


class DetectPancResponseBody(TeaModel):
    def __init__(
        self,
        data: DetectPancResponseBodyData = None,
        message: str = None,
        request_id: str = None,
    ):
        self.data = data
        # 提交异步任务后的提示信息。
        self.message = message
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = DetectPancResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DetectPancResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DetectPancResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DetectPancResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DetectRibFractureRequestURLList(TeaModel):
    def __init__(
        self,
        url: str = None,
    ):
        # This parameter is required.
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.url is not None:
            result['URL'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.url = m.get('URL')
        return self


class DetectRibFractureRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        org_id: str = None,
        org_name: str = None,
        source_type: str = None,
        urllist: List[DetectRibFractureRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.source_type = source_type
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        if self.source_type is not None:
            result['SourceType'] = self.source_type
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        if m.get('SourceType') is not None:
            self.source_type = m.get('SourceType')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = DetectRibFractureRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class DetectRibFractureAdvanceRequestURLList(TeaModel):
    def __init__(
        self,
        urlobject: BinaryIO = None,
    ):
        # This parameter is required.
        self.urlobject = urlobject

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.urlobject is not None:
            result['URL'] = self.urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.urlobject = m.get('URL')
        return self


class DetectRibFractureAdvanceRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        org_id: str = None,
        org_name: str = None,
        source_type: str = None,
        urllist: List[DetectRibFractureAdvanceRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.source_type = source_type
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        if self.source_type is not None:
            result['SourceType'] = self.source_type
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        if m.get('SourceType') is not None:
            self.source_type = m.get('SourceType')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = DetectRibFractureAdvanceRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class DetectRibFractureResponseBodyDataDetections(TeaModel):
    def __init__(
        self,
        coordinate_image: List[int] = None,
        coordinates: List[int] = None,
        frac_sopinstance_uid: str = None,
        fracture_category: str = None,
        fracture_confidence: float = None,
        fracture_id: int = None,
        fracture_location: str = None,
        fracture_segment: int = None,
    ):
        self.coordinate_image = coordinate_image
        self.coordinates = coordinates
        self.frac_sopinstance_uid = frac_sopinstance_uid
        self.fracture_category = fracture_category
        self.fracture_confidence = fracture_confidence
        self.fracture_id = fracture_id
        self.fracture_location = fracture_location
        self.fracture_segment = fracture_segment

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.coordinate_image is not None:
            result['CoordinateImage'] = self.coordinate_image
        if self.coordinates is not None:
            result['Coordinates'] = self.coordinates
        if self.frac_sopinstance_uid is not None:
            result['FracSOPInstanceUID'] = self.frac_sopinstance_uid
        if self.fracture_category is not None:
            result['FractureCategory'] = self.fracture_category
        if self.fracture_confidence is not None:
            result['FractureConfidence'] = self.fracture_confidence
        if self.fracture_id is not None:
            result['FractureId'] = self.fracture_id
        if self.fracture_location is not None:
            result['FractureLocation'] = self.fracture_location
        if self.fracture_segment is not None:
            result['FractureSegment'] = self.fracture_segment
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CoordinateImage') is not None:
            self.coordinate_image = m.get('CoordinateImage')
        if m.get('Coordinates') is not None:
            self.coordinates = m.get('Coordinates')
        if m.get('FracSOPInstanceUID') is not None:
            self.frac_sopinstance_uid = m.get('FracSOPInstanceUID')
        if m.get('FractureCategory') is not None:
            self.fracture_category = m.get('FractureCategory')
        if m.get('FractureConfidence') is not None:
            self.fracture_confidence = m.get('FractureConfidence')
        if m.get('FractureId') is not None:
            self.fracture_id = m.get('FractureId')
        if m.get('FractureLocation') is not None:
            self.fracture_location = m.get('FractureLocation')
        if m.get('FractureSegment') is not None:
            self.fracture_segment = m.get('FractureSegment')
        return self


class DetectRibFractureResponseBodyData(TeaModel):
    def __init__(
        self,
        detections: List[DetectRibFractureResponseBodyDataDetections] = None,
        origin: List[float] = None,
        result_url: str = None,
        spacing: List[float] = None,
    ):
        self.detections = detections
        self.origin = origin
        self.result_url = result_url
        self.spacing = spacing

    def validate(self):
        if self.detections:
            for k in self.detections:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Detections'] = []
        if self.detections is not None:
            for k in self.detections:
                result['Detections'].append(k.to_map() if k else None)
        if self.origin is not None:
            result['Origin'] = self.origin
        if self.result_url is not None:
            result['ResultURL'] = self.result_url
        if self.spacing is not None:
            result['Spacing'] = self.spacing
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.detections = []
        if m.get('Detections') is not None:
            for k in m.get('Detections'):
                temp_model = DetectRibFractureResponseBodyDataDetections()
                self.detections.append(temp_model.from_map(k))
        if m.get('Origin') is not None:
            self.origin = m.get('Origin')
        if m.get('ResultURL') is not None:
            self.result_url = m.get('ResultURL')
        if m.get('Spacing') is not None:
            self.spacing = m.get('Spacing')
        return self


class DetectRibFractureResponseBody(TeaModel):
    def __init__(
        self,
        data: DetectRibFractureResponseBodyData = None,
        message: str = None,
        request_id: str = None,
    ):
        self.data = data
        self.message = message
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = DetectRibFractureResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DetectRibFractureResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DetectRibFractureResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DetectRibFractureResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DetectSkinDiseaseRequest(TeaModel):
    def __init__(
        self,
        org_id: str = None,
        org_name: str = None,
        url: str = None,
    ):
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        if self.url is not None:
            result['Url'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        return self


class DetectSkinDiseaseAdvanceRequest(TeaModel):
    def __init__(
        self,
        org_id: str = None,
        org_name: str = None,
        url_object: BinaryIO = None,
    ):
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.url_object = url_object

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        if self.url_object is not None:
            result['Url'] = self.url_object
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        if m.get('Url') is not None:
            self.url_object = m.get('Url')
        return self


class DetectSkinDiseaseResponseBodyData(TeaModel):
    def __init__(
        self,
        body_part: str = None,
        image_quality: float = None,
        image_type: str = None,
        results: Dict[str, Any] = None,
        results_english: Dict[str, Any] = None,
    ):
        self.body_part = body_part
        self.image_quality = image_quality
        self.image_type = image_type
        self.results = results
        self.results_english = results_english

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.body_part is not None:
            result['BodyPart'] = self.body_part
        if self.image_quality is not None:
            result['ImageQuality'] = self.image_quality
        if self.image_type is not None:
            result['ImageType'] = self.image_type
        if self.results is not None:
            result['Results'] = self.results
        if self.results_english is not None:
            result['ResultsEnglish'] = self.results_english
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BodyPart') is not None:
            self.body_part = m.get('BodyPart')
        if m.get('ImageQuality') is not None:
            self.image_quality = m.get('ImageQuality')
        if m.get('ImageType') is not None:
            self.image_type = m.get('ImageType')
        if m.get('Results') is not None:
            self.results = m.get('Results')
        if m.get('ResultsEnglish') is not None:
            self.results_english = m.get('ResultsEnglish')
        return self


class DetectSkinDiseaseResponseBody(TeaModel):
    def __init__(
        self,
        data: DetectSkinDiseaseResponseBodyData = None,
        request_id: str = None,
    ):
        self.data = data
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = DetectSkinDiseaseResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DetectSkinDiseaseResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: DetectSkinDiseaseResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = DetectSkinDiseaseResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class FeedbackSessionRequest(TeaModel):
    def __init__(
        self,
        feedback: str = None,
        session_id: str = None,
    ):
        # This parameter is required.
        self.feedback = feedback
        # This parameter is required.
        self.session_id = session_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.feedback is not None:
            result['Feedback'] = self.feedback
        if self.session_id is not None:
            result['SessionId'] = self.session_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Feedback') is not None:
            self.feedback = m.get('Feedback')
        if m.get('SessionId') is not None:
            self.session_id = m.get('SessionId')
        return self


class FeedbackSessionResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class FeedbackSessionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: FeedbackSessionResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = FeedbackSessionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GenerateReportRequestReportConfigs(TeaModel):
    def __init__(
        self,
        action: str = None,
        format: str = None,
        template_version: str = None,
        theme: str = None,
    ):
        self.action = action
        self.format = format
        self.template_version = template_version
        self.theme = theme

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.action is not None:
            result['Action'] = self.action
        if self.format is not None:
            result['Format'] = self.format
        if self.template_version is not None:
            result['TemplateVersion'] = self.template_version
        if self.theme is not None:
            result['Theme'] = self.theme
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Action') is not None:
            self.action = m.get('Action')
        if m.get('Format') is not None:
            self.format = m.get('Format')
        if m.get('TemplateVersion') is not None:
            self.template_version = m.get('TemplateVersion')
        if m.get('Theme') is not None:
            self.theme = m.get('Theme')
        return self


class GenerateReportRequest(TeaModel):
    def __init__(
        self,
        report_configs: List[GenerateReportRequestReportConfigs] = None,
    ):
        self.report_configs = report_configs

    def validate(self):
        if self.report_configs:
            for k in self.report_configs:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['ReportConfigs'] = []
        if self.report_configs is not None:
            for k in self.report_configs:
                result['ReportConfigs'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.report_configs = []
        if m.get('ReportConfigs') is not None:
            for k in m.get('ReportConfigs'):
                temp_model = GenerateReportRequestReportConfigs()
                self.report_configs.append(temp_model.from_map(k))
        return self


class GenerateReportShrinkRequest(TeaModel):
    def __init__(
        self,
        report_configs_shrink: str = None,
    ):
        self.report_configs_shrink = report_configs_shrink

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.report_configs_shrink is not None:
            result['ReportConfigs'] = self.report_configs_shrink
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ReportConfigs') is not None:
            self.report_configs_shrink = m.get('ReportConfigs')
        return self


class GenerateReportResponseBodyData(TeaModel):
    def __init__(
        self,
        action_names: List[str] = None,
        type: str = None,
        url: str = None,
    ):
        self.action_names = action_names
        self.type = type
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.action_names is not None:
            result['ActionNames'] = self.action_names
        if self.type is not None:
            result['Type'] = self.type
        if self.url is not None:
            result['Url'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ActionNames') is not None:
            self.action_names = m.get('ActionNames')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Url') is not None:
            self.url = m.get('Url')
        return self


class GenerateReportResponseBody(TeaModel):
    def __init__(
        self,
        data: List[GenerateReportResponseBodyData] = None,
        message: str = None,
        request_id: str = None,
    ):
        self.data = data
        self.message = message
        self.request_id = request_id

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Data'] = []
        if self.data is not None:
            for k in self.data:
                result['Data'].append(k.to_map() if k else None)
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('Data') is not None:
            for k in m.get('Data'):
                temp_model = GenerateReportResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class GenerateReportResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GenerateReportResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GenerateReportResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetAsyncJobResultRequest(TeaModel):
    def __init__(
        self,
        job_id: str = None,
    ):
        # This parameter is required.
        self.job_id = job_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.job_id is not None:
            result['JobId'] = self.job_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('JobId') is not None:
            self.job_id = m.get('JobId')
        return self


class GetAsyncJobResultResponseBodyData(TeaModel):
    def __init__(
        self,
        error_code: str = None,
        error_message: str = None,
        job_id: str = None,
        result: str = None,
        status: str = None,
    ):
        self.error_code = error_code
        self.error_message = error_message
        self.job_id = job_id
        self.result = result
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.error_code is not None:
            result['ErrorCode'] = self.error_code
        if self.error_message is not None:
            result['ErrorMessage'] = self.error_message
        if self.job_id is not None:
            result['JobId'] = self.job_id
        if self.result is not None:
            result['Result'] = self.result
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ErrorCode') is not None:
            self.error_code = m.get('ErrorCode')
        if m.get('ErrorMessage') is not None:
            self.error_message = m.get('ErrorMessage')
        if m.get('JobId') is not None:
            self.job_id = m.get('JobId')
        if m.get('Result') is not None:
            self.result = m.get('Result')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class GetAsyncJobResultResponseBody(TeaModel):
    def __init__(
        self,
        data: GetAsyncJobResultResponseBodyData = None,
        request_id: str = None,
    ):
        self.data = data
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = GetAsyncJobResultResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class GetAsyncJobResultResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: GetAsyncJobResultResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = GetAsyncJobResultResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PredictCVDRequestURLList(TeaModel):
    def __init__(
        self,
        url: str = None,
    ):
        # This parameter is required.
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.url is not None:
            result['URL'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.url = m.get('URL')
        return self


class PredictCVDRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        data_source_type: str = None,
        org_id: str = None,
        org_name: str = None,
        urllist: List[PredictCVDRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.data_source_type = data_source_type
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.data_source_type is not None:
            result['DataSourceType'] = self.data_source_type
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('DataSourceType') is not None:
            self.data_source_type = m.get('DataSourceType')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = PredictCVDRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class PredictCVDAdvanceRequestURLList(TeaModel):
    def __init__(
        self,
        urlobject: BinaryIO = None,
    ):
        # This parameter is required.
        self.urlobject = urlobject

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.urlobject is not None:
            result['URL'] = self.urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.urlobject = m.get('URL')
        return self


class PredictCVDAdvanceRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        data_source_type: str = None,
        org_id: str = None,
        org_name: str = None,
        urllist: List[PredictCVDAdvanceRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.data_source_type = data_source_type
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.data_source_type is not None:
            result['DataSourceType'] = self.data_source_type
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('DataSourceType') is not None:
            self.data_source_type = m.get('DataSourceType')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = PredictCVDAdvanceRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class PredictCVDResponseBodyDataLesionFeatureScore(TeaModel):
    def __init__(
        self,
        aorta_calcium_score: List[float] = None,
        aorta_calcium_volume: List[float] = None,
        aorta_max_diam: List[float] = None,
        aorta_max_diam_std: List[float] = None,
        aortic_height_index: List[float] = None,
        aortic_tortuosity_index: List[float] = None,
        asc_ao_max_diam: List[float] = None,
        ascend_aorta_length: List[float] = None,
        cardio_thoracic_ratio: List[float] = None,
        chest_width: List[float] = None,
        coronary_calcium_score: List[float] = None,
        coronary_calcium_vol: List[float] = None,
        deep_feature: List[float] = None,
        eat_humean: List[float] = None,
        eat_hustd: List[float] = None,
        eat_volume: List[float] = None,
        heart_long_diam: List[float] = None,
        heart_short_diam: List[float] = None,
        heart_width: List[float] = None,
        left_lung_highatt_ratio: List[float] = None,
        left_lung_lowatt_ratio: List[float] = None,
        myo_epi_ratio: List[float] = None,
        right_lung_highatt_ratio: List[float] = None,
        right_lung_lowatt_ratio: List[float] = None,
    ):
        self.aorta_calcium_score = aorta_calcium_score
        self.aorta_calcium_volume = aorta_calcium_volume
        self.aorta_max_diam = aorta_max_diam
        self.aorta_max_diam_std = aorta_max_diam_std
        self.aortic_height_index = aortic_height_index
        self.aortic_tortuosity_index = aortic_tortuosity_index
        self.asc_ao_max_diam = asc_ao_max_diam
        self.ascend_aorta_length = ascend_aorta_length
        self.cardio_thoracic_ratio = cardio_thoracic_ratio
        self.chest_width = chest_width
        self.coronary_calcium_score = coronary_calcium_score
        self.coronary_calcium_vol = coronary_calcium_vol
        self.deep_feature = deep_feature
        self.eat_humean = eat_humean
        self.eat_hustd = eat_hustd
        self.eat_volume = eat_volume
        self.heart_long_diam = heart_long_diam
        self.heart_short_diam = heart_short_diam
        self.heart_width = heart_width
        self.left_lung_highatt_ratio = left_lung_highatt_ratio
        self.left_lung_lowatt_ratio = left_lung_lowatt_ratio
        self.myo_epi_ratio = myo_epi_ratio
        self.right_lung_highatt_ratio = right_lung_highatt_ratio
        self.right_lung_lowatt_ratio = right_lung_lowatt_ratio

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.aorta_calcium_score is not None:
            result['AortaCalciumScore'] = self.aorta_calcium_score
        if self.aorta_calcium_volume is not None:
            result['AortaCalciumVolume'] = self.aorta_calcium_volume
        if self.aorta_max_diam is not None:
            result['AortaMaxDiam'] = self.aorta_max_diam
        if self.aorta_max_diam_std is not None:
            result['AortaMaxDiamStd'] = self.aorta_max_diam_std
        if self.aortic_height_index is not None:
            result['AorticHeightIndex'] = self.aortic_height_index
        if self.aortic_tortuosity_index is not None:
            result['AorticTortuosityIndex'] = self.aortic_tortuosity_index
        if self.asc_ao_max_diam is not None:
            result['AscAoMaxDiam'] = self.asc_ao_max_diam
        if self.ascend_aorta_length is not None:
            result['AscendAortaLength'] = self.ascend_aorta_length
        if self.cardio_thoracic_ratio is not None:
            result['CardioThoracicRatio'] = self.cardio_thoracic_ratio
        if self.chest_width is not None:
            result['ChestWidth'] = self.chest_width
        if self.coronary_calcium_score is not None:
            result['CoronaryCalciumScore'] = self.coronary_calcium_score
        if self.coronary_calcium_vol is not None:
            result['CoronaryCalciumVol'] = self.coronary_calcium_vol
        if self.deep_feature is not None:
            result['DeepFeature'] = self.deep_feature
        if self.eat_humean is not None:
            result['EatHUMean'] = self.eat_humean
        if self.eat_hustd is not None:
            result['EatHUSTD'] = self.eat_hustd
        if self.eat_volume is not None:
            result['EatVolume'] = self.eat_volume
        if self.heart_long_diam is not None:
            result['HeartLongDiam'] = self.heart_long_diam
        if self.heart_short_diam is not None:
            result['HeartShortDiam'] = self.heart_short_diam
        if self.heart_width is not None:
            result['HeartWidth'] = self.heart_width
        if self.left_lung_highatt_ratio is not None:
            result['LeftLungHighattRatio'] = self.left_lung_highatt_ratio
        if self.left_lung_lowatt_ratio is not None:
            result['LeftLungLowattRatio'] = self.left_lung_lowatt_ratio
        if self.myo_epi_ratio is not None:
            result['MyoEpiRatio'] = self.myo_epi_ratio
        if self.right_lung_highatt_ratio is not None:
            result['RightLungHighattRatio'] = self.right_lung_highatt_ratio
        if self.right_lung_lowatt_ratio is not None:
            result['RightLungLowattRatio'] = self.right_lung_lowatt_ratio
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AortaCalciumScore') is not None:
            self.aorta_calcium_score = m.get('AortaCalciumScore')
        if m.get('AortaCalciumVolume') is not None:
            self.aorta_calcium_volume = m.get('AortaCalciumVolume')
        if m.get('AortaMaxDiam') is not None:
            self.aorta_max_diam = m.get('AortaMaxDiam')
        if m.get('AortaMaxDiamStd') is not None:
            self.aorta_max_diam_std = m.get('AortaMaxDiamStd')
        if m.get('AorticHeightIndex') is not None:
            self.aortic_height_index = m.get('AorticHeightIndex')
        if m.get('AorticTortuosityIndex') is not None:
            self.aortic_tortuosity_index = m.get('AorticTortuosityIndex')
        if m.get('AscAoMaxDiam') is not None:
            self.asc_ao_max_diam = m.get('AscAoMaxDiam')
        if m.get('AscendAortaLength') is not None:
            self.ascend_aorta_length = m.get('AscendAortaLength')
        if m.get('CardioThoracicRatio') is not None:
            self.cardio_thoracic_ratio = m.get('CardioThoracicRatio')
        if m.get('ChestWidth') is not None:
            self.chest_width = m.get('ChestWidth')
        if m.get('CoronaryCalciumScore') is not None:
            self.coronary_calcium_score = m.get('CoronaryCalciumScore')
        if m.get('CoronaryCalciumVol') is not None:
            self.coronary_calcium_vol = m.get('CoronaryCalciumVol')
        if m.get('DeepFeature') is not None:
            self.deep_feature = m.get('DeepFeature')
        if m.get('EatHUMean') is not None:
            self.eat_humean = m.get('EatHUMean')
        if m.get('EatHUSTD') is not None:
            self.eat_hustd = m.get('EatHUSTD')
        if m.get('EatVolume') is not None:
            self.eat_volume = m.get('EatVolume')
        if m.get('HeartLongDiam') is not None:
            self.heart_long_diam = m.get('HeartLongDiam')
        if m.get('HeartShortDiam') is not None:
            self.heart_short_diam = m.get('HeartShortDiam')
        if m.get('HeartWidth') is not None:
            self.heart_width = m.get('HeartWidth')
        if m.get('LeftLungHighattRatio') is not None:
            self.left_lung_highatt_ratio = m.get('LeftLungHighattRatio')
        if m.get('LeftLungLowattRatio') is not None:
            self.left_lung_lowatt_ratio = m.get('LeftLungLowattRatio')
        if m.get('MyoEpiRatio') is not None:
            self.myo_epi_ratio = m.get('MyoEpiRatio')
        if m.get('RightLungHighattRatio') is not None:
            self.right_lung_highatt_ratio = m.get('RightLungHighattRatio')
        if m.get('RightLungLowattRatio') is not None:
            self.right_lung_lowatt_ratio = m.get('RightLungLowattRatio')
        return self


class PredictCVDResponseBodyDataLesion(TeaModel):
    def __init__(
        self,
        cvdprobability: float = None,
        feature_score: PredictCVDResponseBodyDataLesionFeatureScore = None,
        images_url: str = None,
        result_url: List[str] = None,
    ):
        self.cvdprobability = cvdprobability
        self.feature_score = feature_score
        self.images_url = images_url
        self.result_url = result_url

    def validate(self):
        if self.feature_score:
            self.feature_score.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cvdprobability is not None:
            result['CVDProbability'] = self.cvdprobability
        if self.feature_score is not None:
            result['FeatureScore'] = self.feature_score.to_map()
        if self.images_url is not None:
            result['ImagesURL'] = self.images_url
        if self.result_url is not None:
            result['ResultURL'] = self.result_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CVDProbability') is not None:
            self.cvdprobability = m.get('CVDProbability')
        if m.get('FeatureScore') is not None:
            temp_model = PredictCVDResponseBodyDataLesionFeatureScore()
            self.feature_score = temp_model.from_map(m['FeatureScore'])
        if m.get('ImagesURL') is not None:
            self.images_url = m.get('ImagesURL')
        if m.get('ResultURL') is not None:
            self.result_url = m.get('ResultURL')
        return self


class PredictCVDResponseBodyData(TeaModel):
    def __init__(
        self,
        lesion: PredictCVDResponseBodyDataLesion = None,
    ):
        self.lesion = lesion

    def validate(self):
        if self.lesion:
            self.lesion.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lesion is not None:
            result['Lesion'] = self.lesion.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lesion') is not None:
            temp_model = PredictCVDResponseBodyDataLesion()
            self.lesion = temp_model.from_map(m['Lesion'])
        return self


class PredictCVDResponseBody(TeaModel):
    def __init__(
        self,
        data: PredictCVDResponseBodyData = None,
        message: str = None,
        request_id: str = None,
    ):
        self.data = data
        self.message = message
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = PredictCVDResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class PredictCVDResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: PredictCVDResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = PredictCVDResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RunCTRegistrationRequestFloatingList(TeaModel):
    def __init__(
        self,
        floating_url: str = None,
    ):
        # This parameter is required.
        self.floating_url = floating_url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.floating_url is not None:
            result['FloatingURL'] = self.floating_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FloatingURL') is not None:
            self.floating_url = m.get('FloatingURL')
        return self


class RunCTRegistrationRequestReferenceList(TeaModel):
    def __init__(
        self,
        reference_url: str = None,
    ):
        # This parameter is required.
        self.reference_url = reference_url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.reference_url is not None:
            result['ReferenceURL'] = self.reference_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ReferenceURL') is not None:
            self.reference_url = m.get('ReferenceURL')
        return self


class RunCTRegistrationRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        data_source_type: str = None,
        floating_list: List[RunCTRegistrationRequestFloatingList] = None,
        org_id: str = None,
        org_name: str = None,
        reference_list: List[RunCTRegistrationRequestReferenceList] = None,
    ):
        # DICOM。
        # 
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.data_source_type = data_source_type
        # This parameter is required.
        self.floating_list = floating_list
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.reference_list = reference_list

    def validate(self):
        if self.floating_list:
            for k in self.floating_list:
                if k:
                    k.validate()
        if self.reference_list:
            for k in self.reference_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.data_source_type is not None:
            result['DataSourceType'] = self.data_source_type
        result['FloatingList'] = []
        if self.floating_list is not None:
            for k in self.floating_list:
                result['FloatingList'].append(k.to_map() if k else None)
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        result['ReferenceList'] = []
        if self.reference_list is not None:
            for k in self.reference_list:
                result['ReferenceList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('DataSourceType') is not None:
            self.data_source_type = m.get('DataSourceType')
        self.floating_list = []
        if m.get('FloatingList') is not None:
            for k in m.get('FloatingList'):
                temp_model = RunCTRegistrationRequestFloatingList()
                self.floating_list.append(temp_model.from_map(k))
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        self.reference_list = []
        if m.get('ReferenceList') is not None:
            for k in m.get('ReferenceList'):
                temp_model = RunCTRegistrationRequestReferenceList()
                self.reference_list.append(temp_model.from_map(k))
        return self


class RunCTRegistrationAdvanceRequestFloatingList(TeaModel):
    def __init__(
        self,
        floating_urlobject: BinaryIO = None,
    ):
        # This parameter is required.
        self.floating_urlobject = floating_urlobject

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.floating_urlobject is not None:
            result['FloatingURL'] = self.floating_urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FloatingURL') is not None:
            self.floating_urlobject = m.get('FloatingURL')
        return self


class RunCTRegistrationAdvanceRequestReferenceList(TeaModel):
    def __init__(
        self,
        reference_urlobject: BinaryIO = None,
    ):
        # This parameter is required.
        self.reference_urlobject = reference_urlobject

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.reference_urlobject is not None:
            result['ReferenceURL'] = self.reference_urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ReferenceURL') is not None:
            self.reference_urlobject = m.get('ReferenceURL')
        return self


class RunCTRegistrationAdvanceRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        data_source_type: str = None,
        floating_list: List[RunCTRegistrationAdvanceRequestFloatingList] = None,
        org_id: str = None,
        org_name: str = None,
        reference_list: List[RunCTRegistrationAdvanceRequestReferenceList] = None,
    ):
        # DICOM。
        # 
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.data_source_type = data_source_type
        # This parameter is required.
        self.floating_list = floating_list
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.reference_list = reference_list

    def validate(self):
        if self.floating_list:
            for k in self.floating_list:
                if k:
                    k.validate()
        if self.reference_list:
            for k in self.reference_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.data_source_type is not None:
            result['DataSourceType'] = self.data_source_type
        result['FloatingList'] = []
        if self.floating_list is not None:
            for k in self.floating_list:
                result['FloatingList'].append(k.to_map() if k else None)
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        result['ReferenceList'] = []
        if self.reference_list is not None:
            for k in self.reference_list:
                result['ReferenceList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('DataSourceType') is not None:
            self.data_source_type = m.get('DataSourceType')
        self.floating_list = []
        if m.get('FloatingList') is not None:
            for k in m.get('FloatingList'):
                temp_model = RunCTRegistrationAdvanceRequestFloatingList()
                self.floating_list.append(temp_model.from_map(k))
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        self.reference_list = []
        if m.get('ReferenceList') is not None:
            for k in m.get('ReferenceList'):
                temp_model = RunCTRegistrationAdvanceRequestReferenceList()
                self.reference_list.append(temp_model.from_map(k))
        return self


class RunCTRegistrationResponseBodyData(TeaModel):
    def __init__(
        self,
        durl: str = None,
        nurl: str = None,
    ):
        self.durl = durl
        self.nurl = nurl

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.durl is not None:
            result['DUrl'] = self.durl
        if self.nurl is not None:
            result['NUrl'] = self.nurl
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DUrl') is not None:
            self.durl = m.get('DUrl')
        if m.get('NUrl') is not None:
            self.nurl = m.get('NUrl')
        return self


class RunCTRegistrationResponseBody(TeaModel):
    def __init__(
        self,
        data: RunCTRegistrationResponseBodyData = None,
        message: str = None,
        request_id: str = None,
    ):
        self.data = data
        self.message = message
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = RunCTRegistrationResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class RunCTRegistrationResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: RunCTRegistrationResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = RunCTRegistrationResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RunMedQARequestAnswerImageDataList(TeaModel):
    def __init__(
        self,
        answer_image_data: str = None,
    ):
        self.answer_image_data = answer_image_data

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.answer_image_data is not None:
            result['AnswerImageData'] = self.answer_image_data
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AnswerImageData') is not None:
            self.answer_image_data = m.get('AnswerImageData')
        return self


class RunMedQARequestAnswerImageURLList(TeaModel):
    def __init__(
        self,
        answer_image_url: str = None,
    ):
        self.answer_image_url = answer_image_url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.answer_image_url is not None:
            result['AnswerImageURL'] = self.answer_image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AnswerImageURL') is not None:
            self.answer_image_url = m.get('AnswerImageURL')
        return self


class RunMedQARequestAnswerTextList(TeaModel):
    def __init__(
        self,
        answer_text: str = None,
    ):
        self.answer_text = answer_text

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.answer_text is not None:
            result['AnswerText'] = self.answer_text
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AnswerText') is not None:
            self.answer_text = m.get('AnswerText')
        return self


class RunMedQARequest(TeaModel):
    def __init__(
        self,
        answer_image_data_list: List[RunMedQARequestAnswerImageDataList] = None,
        answer_image_urllist: List[RunMedQARequestAnswerImageURLList] = None,
        answer_text_list: List[RunMedQARequestAnswerTextList] = None,
        department: str = None,
        org_id: str = None,
        org_name: str = None,
        question_type: str = None,
        session_id: str = None,
    ):
        self.answer_image_data_list = answer_image_data_list
        self.answer_image_urllist = answer_image_urllist
        self.answer_text_list = answer_text_list
        # This parameter is required.
        self.department = department
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.question_type = question_type
        self.session_id = session_id

    def validate(self):
        if self.answer_image_data_list:
            for k in self.answer_image_data_list:
                if k:
                    k.validate()
        if self.answer_image_urllist:
            for k in self.answer_image_urllist:
                if k:
                    k.validate()
        if self.answer_text_list:
            for k in self.answer_text_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['AnswerImageDataList'] = []
        if self.answer_image_data_list is not None:
            for k in self.answer_image_data_list:
                result['AnswerImageDataList'].append(k.to_map() if k else None)
        result['AnswerImageURLList'] = []
        if self.answer_image_urllist is not None:
            for k in self.answer_image_urllist:
                result['AnswerImageURLList'].append(k.to_map() if k else None)
        result['AnswerTextList'] = []
        if self.answer_text_list is not None:
            for k in self.answer_text_list:
                result['AnswerTextList'].append(k.to_map() if k else None)
        if self.department is not None:
            result['Department'] = self.department
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        if self.question_type is not None:
            result['QuestionType'] = self.question_type
        if self.session_id is not None:
            result['SessionId'] = self.session_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.answer_image_data_list = []
        if m.get('AnswerImageDataList') is not None:
            for k in m.get('AnswerImageDataList'):
                temp_model = RunMedQARequestAnswerImageDataList()
                self.answer_image_data_list.append(temp_model.from_map(k))
        self.answer_image_urllist = []
        if m.get('AnswerImageURLList') is not None:
            for k in m.get('AnswerImageURLList'):
                temp_model = RunMedQARequestAnswerImageURLList()
                self.answer_image_urllist.append(temp_model.from_map(k))
        self.answer_text_list = []
        if m.get('AnswerTextList') is not None:
            for k in m.get('AnswerTextList'):
                temp_model = RunMedQARequestAnswerTextList()
                self.answer_text_list.append(temp_model.from_map(k))
        if m.get('Department') is not None:
            self.department = m.get('Department')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        if m.get('QuestionType') is not None:
            self.question_type = m.get('QuestionType')
        if m.get('SessionId') is not None:
            self.session_id = m.get('SessionId')
        return self


class RunMedQAAdvanceRequestAnswerImageDataList(TeaModel):
    def __init__(
        self,
        answer_image_data: str = None,
    ):
        self.answer_image_data = answer_image_data

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.answer_image_data is not None:
            result['AnswerImageData'] = self.answer_image_data
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AnswerImageData') is not None:
            self.answer_image_data = m.get('AnswerImageData')
        return self


class RunMedQAAdvanceRequestAnswerImageURLList(TeaModel):
    def __init__(
        self,
        answer_image_urlobject: BinaryIO = None,
    ):
        self.answer_image_urlobject = answer_image_urlobject

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.answer_image_urlobject is not None:
            result['AnswerImageURL'] = self.answer_image_urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AnswerImageURL') is not None:
            self.answer_image_urlobject = m.get('AnswerImageURL')
        return self


class RunMedQAAdvanceRequestAnswerTextList(TeaModel):
    def __init__(
        self,
        answer_text: str = None,
    ):
        self.answer_text = answer_text

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.answer_text is not None:
            result['AnswerText'] = self.answer_text
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AnswerText') is not None:
            self.answer_text = m.get('AnswerText')
        return self


class RunMedQAAdvanceRequest(TeaModel):
    def __init__(
        self,
        answer_image_data_list: List[RunMedQAAdvanceRequestAnswerImageDataList] = None,
        answer_image_urllist: List[RunMedQAAdvanceRequestAnswerImageURLList] = None,
        answer_text_list: List[RunMedQAAdvanceRequestAnswerTextList] = None,
        department: str = None,
        org_id: str = None,
        org_name: str = None,
        question_type: str = None,
        session_id: str = None,
    ):
        self.answer_image_data_list = answer_image_data_list
        self.answer_image_urllist = answer_image_urllist
        self.answer_text_list = answer_text_list
        # This parameter is required.
        self.department = department
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.question_type = question_type
        self.session_id = session_id

    def validate(self):
        if self.answer_image_data_list:
            for k in self.answer_image_data_list:
                if k:
                    k.validate()
        if self.answer_image_urllist:
            for k in self.answer_image_urllist:
                if k:
                    k.validate()
        if self.answer_text_list:
            for k in self.answer_text_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['AnswerImageDataList'] = []
        if self.answer_image_data_list is not None:
            for k in self.answer_image_data_list:
                result['AnswerImageDataList'].append(k.to_map() if k else None)
        result['AnswerImageURLList'] = []
        if self.answer_image_urllist is not None:
            for k in self.answer_image_urllist:
                result['AnswerImageURLList'].append(k.to_map() if k else None)
        result['AnswerTextList'] = []
        if self.answer_text_list is not None:
            for k in self.answer_text_list:
                result['AnswerTextList'].append(k.to_map() if k else None)
        if self.department is not None:
            result['Department'] = self.department
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        if self.question_type is not None:
            result['QuestionType'] = self.question_type
        if self.session_id is not None:
            result['SessionId'] = self.session_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.answer_image_data_list = []
        if m.get('AnswerImageDataList') is not None:
            for k in m.get('AnswerImageDataList'):
                temp_model = RunMedQAAdvanceRequestAnswerImageDataList()
                self.answer_image_data_list.append(temp_model.from_map(k))
        self.answer_image_urllist = []
        if m.get('AnswerImageURLList') is not None:
            for k in m.get('AnswerImageURLList'):
                temp_model = RunMedQAAdvanceRequestAnswerImageURLList()
                self.answer_image_urllist.append(temp_model.from_map(k))
        self.answer_text_list = []
        if m.get('AnswerTextList') is not None:
            for k in m.get('AnswerTextList'):
                temp_model = RunMedQAAdvanceRequestAnswerTextList()
                self.answer_text_list.append(temp_model.from_map(k))
        if m.get('Department') is not None:
            self.department = m.get('Department')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        if m.get('QuestionType') is not None:
            self.question_type = m.get('QuestionType')
        if m.get('SessionId') is not None:
            self.session_id = m.get('SessionId')
        return self


class RunMedQAResponseBodyData(TeaModel):
    def __init__(
        self,
        answer_type: str = None,
        options: List[str] = None,
        question: str = None,
        question_type: str = None,
        reports: Dict[str, str] = None,
        session_id: str = None,
    ):
        self.answer_type = answer_type
        self.options = options
        self.question = question
        self.question_type = question_type
        self.reports = reports
        self.session_id = session_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.answer_type is not None:
            result['AnswerType'] = self.answer_type
        if self.options is not None:
            result['Options'] = self.options
        if self.question is not None:
            result['Question'] = self.question
        if self.question_type is not None:
            result['QuestionType'] = self.question_type
        if self.reports is not None:
            result['Reports'] = self.reports
        if self.session_id is not None:
            result['SessionId'] = self.session_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AnswerType') is not None:
            self.answer_type = m.get('AnswerType')
        if m.get('Options') is not None:
            self.options = m.get('Options')
        if m.get('Question') is not None:
            self.question = m.get('Question')
        if m.get('QuestionType') is not None:
            self.question_type = m.get('QuestionType')
        if m.get('Reports') is not None:
            self.reports = m.get('Reports')
        if m.get('SessionId') is not None:
            self.session_id = m.get('SessionId')
        return self


class RunMedQAResponseBody(TeaModel):
    def __init__(
        self,
        data: RunMedQAResponseBodyData = None,
        request_id: str = None,
    ):
        self.data = data
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = RunMedQAResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class RunMedQAResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: RunMedQAResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = RunMedQAResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ScreenCRCRequestURLList(TeaModel):
    def __init__(
        self,
        url: str = None,
    ):
        # This parameter is required.
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.url is not None:
            result['URL'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.url = m.get('URL')
        return self


class ScreenCRCRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        data_source_type: str = None,
        org_id: str = None,
        org_name: str = None,
        urllist: List[ScreenCRCRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.data_source_type = data_source_type
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.data_source_type is not None:
            result['DataSourceType'] = self.data_source_type
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('DataSourceType') is not None:
            self.data_source_type = m.get('DataSourceType')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = ScreenCRCRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class ScreenCRCAdvanceRequestURLList(TeaModel):
    def __init__(
        self,
        urlobject: BinaryIO = None,
    ):
        # This parameter is required.
        self.urlobject = urlobject

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.urlobject is not None:
            result['URL'] = self.urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.urlobject = m.get('URL')
        return self


class ScreenCRCAdvanceRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        data_source_type: str = None,
        org_id: str = None,
        org_name: str = None,
        urllist: List[ScreenCRCAdvanceRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.data_source_type = data_source_type
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.data_source_type is not None:
            result['DataSourceType'] = self.data_source_type
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('DataSourceType') is not None:
            self.data_source_type = m.get('DataSourceType')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = ScreenCRCAdvanceRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class ScreenCRCResponseBodyDataLesion(TeaModel):
    def __init__(
        self,
        crcvolume: str = None,
        colorectum_volume: str = None,
        mask: str = None,
        probabilities: str = None,
    ):
        self.crcvolume = crcvolume
        self.colorectum_volume = colorectum_volume
        self.mask = mask
        self.probabilities = probabilities

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.crcvolume is not None:
            result['CRCVolume'] = self.crcvolume
        if self.colorectum_volume is not None:
            result['ColorectumVolume'] = self.colorectum_volume
        if self.mask is not None:
            result['Mask'] = self.mask
        if self.probabilities is not None:
            result['Probabilities'] = self.probabilities
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CRCVolume') is not None:
            self.crcvolume = m.get('CRCVolume')
        if m.get('ColorectumVolume') is not None:
            self.colorectum_volume = m.get('ColorectumVolume')
        if m.get('Mask') is not None:
            self.mask = m.get('Mask')
        if m.get('Probabilities') is not None:
            self.probabilities = m.get('Probabilities')
        return self


class ScreenCRCResponseBodyData(TeaModel):
    def __init__(
        self,
        lesion: ScreenCRCResponseBodyDataLesion = None,
    ):
        self.lesion = lesion

    def validate(self):
        if self.lesion:
            self.lesion.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lesion is not None:
            result['Lesion'] = self.lesion.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lesion') is not None:
            temp_model = ScreenCRCResponseBodyDataLesion()
            self.lesion = temp_model.from_map(m['Lesion'])
        return self


class ScreenCRCResponseBody(TeaModel):
    def __init__(
        self,
        data: ScreenCRCResponseBodyData = None,
        message: str = None,
        request_id: str = None,
    ):
        self.data = data
        self.message = message
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = ScreenCRCResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ScreenCRCResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ScreenCRCResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ScreenCRCResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ScreenChestCTRequestURLList(TeaModel):
    def __init__(
        self,
        url: str = None,
    ):
        # This parameter is required.
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.url is not None:
            result['URL'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.url = m.get('URL')
        return self


class ScreenChestCTRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        mask: int = None,
        org_id: str = None,
        org_name: str = None,
        urllist: List[ScreenChestCTRequestURLList] = None,
        verbose: int = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        self.mask = mask
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.urllist = urllist
        self.verbose = verbose

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.mask is not None:
            result['Mask'] = self.mask
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        if self.verbose is not None:
            result['Verbose'] = self.verbose
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('Mask') is not None:
            self.mask = m.get('Mask')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = ScreenChestCTRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        if m.get('Verbose') is not None:
            self.verbose = m.get('Verbose')
        return self


class ScreenChestCTAdvanceRequestURLList(TeaModel):
    def __init__(
        self,
        urlobject: BinaryIO = None,
    ):
        # This parameter is required.
        self.urlobject = urlobject

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.urlobject is not None:
            result['URL'] = self.urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.urlobject = m.get('URL')
        return self


class ScreenChestCTAdvanceRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        mask: int = None,
        org_id: str = None,
        org_name: str = None,
        urllist: List[ScreenChestCTAdvanceRequestURLList] = None,
        verbose: int = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        self.mask = mask
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.urllist = urllist
        self.verbose = verbose

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.mask is not None:
            result['Mask'] = self.mask
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        if self.verbose is not None:
            result['Verbose'] = self.verbose
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('Mask') is not None:
            self.mask = m.get('Mask')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = ScreenChestCTAdvanceRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        if m.get('Verbose') is not None:
            self.verbose = m.get('Verbose')
        return self


class ScreenChestCTResponseBodyDataAnalyzeChestVesselAortaInfo(TeaModel):
    def __init__(
        self,
        area: List[float] = None,
        coordinates: List[List[float]] = None,
        label_value: int = None,
        max_area: float = None,
        max_area_index: int = None,
        max_diameter: float = None,
    ):
        # 1
        self.area = area
        self.coordinates = coordinates
        self.label_value = label_value
        self.max_area = max_area
        self.max_area_index = max_area_index
        self.max_diameter = max_diameter

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.area is not None:
            result['Area'] = self.area
        if self.coordinates is not None:
            result['Coordinates'] = self.coordinates
        if self.label_value is not None:
            result['LabelValue'] = self.label_value
        if self.max_area is not None:
            result['MaxArea'] = self.max_area
        if self.max_area_index is not None:
            result['MaxAreaIndex'] = self.max_area_index
        if self.max_diameter is not None:
            result['MaxDiameter'] = self.max_diameter
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Area') is not None:
            self.area = m.get('Area')
        if m.get('Coordinates') is not None:
            self.coordinates = m.get('Coordinates')
        if m.get('LabelValue') is not None:
            self.label_value = m.get('LabelValue')
        if m.get('MaxArea') is not None:
            self.max_area = m.get('MaxArea')
        if m.get('MaxAreaIndex') is not None:
            self.max_area_index = m.get('MaxAreaIndex')
        if m.get('MaxDiameter') is not None:
            self.max_diameter = m.get('MaxDiameter')
        return self


class ScreenChestCTResponseBodyDataAnalyzeChestVesselPulmonaryInfo(TeaModel):
    def __init__(
        self,
        area: List[float] = None,
        coordinates: List[List[float]] = None,
        label_value: int = None,
        max_area: float = None,
        max_area_index: int = None,
        max_diameter: float = None,
        nearest_aorta_area: float = None,
    ):
        # 1
        self.area = area
        self.coordinates = coordinates
        self.label_value = label_value
        self.max_area = max_area
        self.max_area_index = max_area_index
        self.max_diameter = max_diameter
        self.nearest_aorta_area = nearest_aorta_area

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.area is not None:
            result['Area'] = self.area
        if self.coordinates is not None:
            result['Coordinates'] = self.coordinates
        if self.label_value is not None:
            result['LabelValue'] = self.label_value
        if self.max_area is not None:
            result['MaxArea'] = self.max_area
        if self.max_area_index is not None:
            result['MaxAreaIndex'] = self.max_area_index
        if self.max_diameter is not None:
            result['MaxDiameter'] = self.max_diameter
        if self.nearest_aorta_area is not None:
            result['NearestAortaArea'] = self.nearest_aorta_area
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Area') is not None:
            self.area = m.get('Area')
        if m.get('Coordinates') is not None:
            self.coordinates = m.get('Coordinates')
        if m.get('LabelValue') is not None:
            self.label_value = m.get('LabelValue')
        if m.get('MaxArea') is not None:
            self.max_area = m.get('MaxArea')
        if m.get('MaxAreaIndex') is not None:
            self.max_area_index = m.get('MaxAreaIndex')
        if m.get('MaxDiameter') is not None:
            self.max_diameter = m.get('MaxDiameter')
        if m.get('NearestAortaArea') is not None:
            self.nearest_aorta_area = m.get('NearestAortaArea')
        return self


class ScreenChestCTResponseBodyDataAnalyzeChestVessel(TeaModel):
    def __init__(
        self,
        aorta_info: ScreenChestCTResponseBodyDataAnalyzeChestVesselAortaInfo = None,
        pulmonary_info: ScreenChestCTResponseBodyDataAnalyzeChestVesselPulmonaryInfo = None,
        result_url: str = None,
    ):
        self.aorta_info = aorta_info
        self.pulmonary_info = pulmonary_info
        self.result_url = result_url

    def validate(self):
        if self.aorta_info:
            self.aorta_info.validate()
        if self.pulmonary_info:
            self.pulmonary_info.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.aorta_info is not None:
            result['AortaInfo'] = self.aorta_info.to_map()
        if self.pulmonary_info is not None:
            result['PulmonaryInfo'] = self.pulmonary_info.to_map()
        if self.result_url is not None:
            result['ResultURL'] = self.result_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AortaInfo') is not None:
            temp_model = ScreenChestCTResponseBodyDataAnalyzeChestVesselAortaInfo()
            self.aorta_info = temp_model.from_map(m['AortaInfo'])
        if m.get('PulmonaryInfo') is not None:
            temp_model = ScreenChestCTResponseBodyDataAnalyzeChestVesselPulmonaryInfo()
            self.pulmonary_info = temp_model.from_map(m['PulmonaryInfo'])
        if m.get('ResultURL') is not None:
            self.result_url = m.get('ResultURL')
        return self


class ScreenChestCTResponseBodyDataCACSDetections(TeaModel):
    def __init__(
        self,
        calcium_center: List[int] = None,
        calcium_id: int = None,
        calcium_score: float = None,
        calcium_volume: float = None,
    ):
        self.calcium_center = calcium_center
        self.calcium_id = calcium_id
        self.calcium_score = calcium_score
        self.calcium_volume = calcium_volume

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.calcium_center is not None:
            result['CalciumCenter'] = self.calcium_center
        if self.calcium_id is not None:
            result['CalciumId'] = self.calcium_id
        if self.calcium_score is not None:
            result['CalciumScore'] = self.calcium_score
        if self.calcium_volume is not None:
            result['CalciumVolume'] = self.calcium_volume
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CalciumCenter') is not None:
            self.calcium_center = m.get('CalciumCenter')
        if m.get('CalciumId') is not None:
            self.calcium_id = m.get('CalciumId')
        if m.get('CalciumScore') is not None:
            self.calcium_score = m.get('CalciumScore')
        if m.get('CalciumVolume') is not None:
            self.calcium_volume = m.get('CalciumVolume')
        return self


class ScreenChestCTResponseBodyDataCACS(TeaModel):
    def __init__(
        self,
        detections: List[ScreenChestCTResponseBodyDataCACSDetections] = None,
        result_url: str = None,
        score: str = None,
        series_instance_uid: str = None,
        volume_score: str = None,
    ):
        self.detections = detections
        self.result_url = result_url
        self.score = score
        self.series_instance_uid = series_instance_uid
        self.volume_score = volume_score

    def validate(self):
        if self.detections:
            for k in self.detections:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Detections'] = []
        if self.detections is not None:
            for k in self.detections:
                result['Detections'].append(k.to_map() if k else None)
        if self.result_url is not None:
            result['ResultUrl'] = self.result_url
        if self.score is not None:
            result['Score'] = self.score
        if self.series_instance_uid is not None:
            result['SeriesInstanceUID'] = self.series_instance_uid
        if self.volume_score is not None:
            result['VolumeScore'] = self.volume_score
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.detections = []
        if m.get('Detections') is not None:
            for k in m.get('Detections'):
                temp_model = ScreenChestCTResponseBodyDataCACSDetections()
                self.detections.append(temp_model.from_map(k))
        if m.get('ResultUrl') is not None:
            self.result_url = m.get('ResultUrl')
        if m.get('Score') is not None:
            self.score = m.get('Score')
        if m.get('SeriesInstanceUID') is not None:
            self.series_instance_uid = m.get('SeriesInstanceUID')
        if m.get('VolumeScore') is not None:
            self.volume_score = m.get('VolumeScore')
        return self


class ScreenChestCTResponseBodyDataCalcBMDDetections(TeaModel):
    def __init__(
        self,
        vert_bmd: float = None,
        vert_category: float = None,
        vert_id: str = None,
        vert_tscore: float = None,
        vert_zscore: float = None,
    ):
        self.vert_bmd = vert_bmd
        self.vert_category = vert_category
        self.vert_id = vert_id
        self.vert_tscore = vert_tscore
        self.vert_zscore = vert_zscore

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.vert_bmd is not None:
            result['VertBMD'] = self.vert_bmd
        if self.vert_category is not None:
            result['VertCategory'] = self.vert_category
        if self.vert_id is not None:
            result['VertId'] = self.vert_id
        if self.vert_tscore is not None:
            result['VertTScore'] = self.vert_tscore
        if self.vert_zscore is not None:
            result['VertZScore'] = self.vert_zscore
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('VertBMD') is not None:
            self.vert_bmd = m.get('VertBMD')
        if m.get('VertCategory') is not None:
            self.vert_category = m.get('VertCategory')
        if m.get('VertId') is not None:
            self.vert_id = m.get('VertId')
        if m.get('VertTScore') is not None:
            self.vert_tscore = m.get('VertTScore')
        if m.get('VertZScore') is not None:
            self.vert_zscore = m.get('VertZScore')
        return self


class ScreenChestCTResponseBodyDataCalcBMD(TeaModel):
    def __init__(
        self,
        detections: List[ScreenChestCTResponseBodyDataCalcBMDDetections] = None,
        origin: List[float] = None,
        result_url: str = None,
        series_instance_uid: str = None,
        spacing: List[float] = None,
    ):
        self.detections = detections
        self.origin = origin
        self.result_url = result_url
        self.series_instance_uid = series_instance_uid
        self.spacing = spacing

    def validate(self):
        if self.detections:
            for k in self.detections:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Detections'] = []
        if self.detections is not None:
            for k in self.detections:
                result['Detections'].append(k.to_map() if k else None)
        if self.origin is not None:
            result['Origin'] = self.origin
        if self.result_url is not None:
            result['ResultURL'] = self.result_url
        if self.series_instance_uid is not None:
            result['SeriesInstanceUid'] = self.series_instance_uid
        if self.spacing is not None:
            result['Spacing'] = self.spacing
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.detections = []
        if m.get('Detections') is not None:
            for k in m.get('Detections'):
                temp_model = ScreenChestCTResponseBodyDataCalcBMDDetections()
                self.detections.append(temp_model.from_map(k))
        if m.get('Origin') is not None:
            self.origin = m.get('Origin')
        if m.get('ResultURL') is not None:
            self.result_url = m.get('ResultURL')
        if m.get('SeriesInstanceUid') is not None:
            self.series_instance_uid = m.get('SeriesInstanceUid')
        if m.get('Spacing') is not None:
            self.spacing = m.get('Spacing')
        return self


class ScreenChestCTResponseBodyDataCovid(TeaModel):
    def __init__(
        self,
        lesion_ratio: str = None,
        mask: str = None,
        new_probability: str = None,
        normal_probability: str = None,
        other_probability: str = None,
        series_instance_uid: str = None,
    ):
        self.lesion_ratio = lesion_ratio
        self.mask = mask
        self.new_probability = new_probability
        self.normal_probability = normal_probability
        self.other_probability = other_probability
        self.series_instance_uid = series_instance_uid

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lesion_ratio is not None:
            result['LesionRatio'] = self.lesion_ratio
        if self.mask is not None:
            result['Mask'] = self.mask
        if self.new_probability is not None:
            result['NewProbability'] = self.new_probability
        if self.normal_probability is not None:
            result['NormalProbability'] = self.normal_probability
        if self.other_probability is not None:
            result['OtherProbability'] = self.other_probability
        if self.series_instance_uid is not None:
            result['SeriesInstanceUID'] = self.series_instance_uid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LesionRatio') is not None:
            self.lesion_ratio = m.get('LesionRatio')
        if m.get('Mask') is not None:
            self.mask = m.get('Mask')
        if m.get('NewProbability') is not None:
            self.new_probability = m.get('NewProbability')
        if m.get('NormalProbability') is not None:
            self.normal_probability = m.get('NormalProbability')
        if m.get('OtherProbability') is not None:
            self.other_probability = m.get('OtherProbability')
        if m.get('SeriesInstanceUID') is not None:
            self.series_instance_uid = m.get('SeriesInstanceUID')
        return self


class ScreenChestCTResponseBodyDataDetectAD(TeaModel):
    def __init__(
        self,
        distance_map: str = None,
        mask: str = None,
        possibility: str = None,
        series_instance_uid: str = None,
        slice_val: int = None,
    ):
        self.distance_map = distance_map
        self.mask = mask
        self.possibility = possibility
        self.series_instance_uid = series_instance_uid
        self.slice_val = slice_val

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.distance_map is not None:
            result['DistanceMap'] = self.distance_map
        if self.mask is not None:
            result['Mask'] = self.mask
        if self.possibility is not None:
            result['Possibility'] = self.possibility
        if self.series_instance_uid is not None:
            result['SeriesInstanceUid'] = self.series_instance_uid
        if self.slice_val is not None:
            result['SliceVal'] = self.slice_val
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DistanceMap') is not None:
            self.distance_map = m.get('DistanceMap')
        if m.get('Mask') is not None:
            self.mask = m.get('Mask')
        if m.get('Possibility') is not None:
            self.possibility = m.get('Possibility')
        if m.get('SeriesInstanceUid') is not None:
            self.series_instance_uid = m.get('SeriesInstanceUid')
        if m.get('SliceVal') is not None:
            self.slice_val = m.get('SliceVal')
        return self


class ScreenChestCTResponseBodyDataDetectLiverSteatosisDetections(TeaModel):
    def __init__(
        self,
        fat_fract: float = None,
        liver_hu: float = None,
        liver_roi1: float = None,
        liver_roi2: float = None,
        liver_roi3: float = None,
        liver_slice: float = None,
        liver_spleen_difference: float = None,
        liver_spleen_ratio: float = None,
        liver_volume: float = None,
        maoss_score: float = None,
        prediction: str = None,
        probability: float = None,
        roi1center: List[int] = None,
        roi2center: List[int] = None,
        roi3center: List[int] = None,
        radius: int = None,
        spleen_center: List[int] = None,
        spleen_hu: float = None,
        spleen_roi: float = None,
        spleen_slice: float = None,
        spleen_volume: float = None,
    ):
        self.fat_fract = fat_fract
        self.liver_hu = liver_hu
        self.liver_roi1 = liver_roi1
        self.liver_roi2 = liver_roi2
        self.liver_roi3 = liver_roi3
        self.liver_slice = liver_slice
        self.liver_spleen_difference = liver_spleen_difference
        self.liver_spleen_ratio = liver_spleen_ratio
        self.liver_volume = liver_volume
        self.maoss_score = maoss_score
        self.prediction = prediction
        self.probability = probability
        self.roi1center = roi1center
        self.roi2center = roi2center
        self.roi3center = roi3center
        self.radius = radius
        self.spleen_center = spleen_center
        self.spleen_hu = spleen_hu
        self.spleen_roi = spleen_roi
        self.spleen_slice = spleen_slice
        self.spleen_volume = spleen_volume

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.fat_fract is not None:
            result['FatFract'] = self.fat_fract
        if self.liver_hu is not None:
            result['LiverHU'] = self.liver_hu
        if self.liver_roi1 is not None:
            result['LiverROI1'] = self.liver_roi1
        if self.liver_roi2 is not None:
            result['LiverROI2'] = self.liver_roi2
        if self.liver_roi3 is not None:
            result['LiverROI3'] = self.liver_roi3
        if self.liver_slice is not None:
            result['LiverSlice'] = self.liver_slice
        if self.liver_spleen_difference is not None:
            result['LiverSpleenDifference'] = self.liver_spleen_difference
        if self.liver_spleen_ratio is not None:
            result['LiverSpleenRatio'] = self.liver_spleen_ratio
        if self.liver_volume is not None:
            result['LiverVolume'] = self.liver_volume
        if self.maoss_score is not None:
            result['MaossScore'] = self.maoss_score
        if self.prediction is not None:
            result['Prediction'] = self.prediction
        if self.probability is not None:
            result['Probability'] = self.probability
        if self.roi1center is not None:
            result['ROI1Center'] = self.roi1center
        if self.roi2center is not None:
            result['ROI2Center'] = self.roi2center
        if self.roi3center is not None:
            result['ROI3Center'] = self.roi3center
        if self.radius is not None:
            result['Radius'] = self.radius
        if self.spleen_center is not None:
            result['SpleenCenter'] = self.spleen_center
        if self.spleen_hu is not None:
            result['SpleenHU'] = self.spleen_hu
        if self.spleen_roi is not None:
            result['SpleenROI'] = self.spleen_roi
        if self.spleen_slice is not None:
            result['SpleenSlice'] = self.spleen_slice
        if self.spleen_volume is not None:
            result['SpleenVolume'] = self.spleen_volume
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FatFract') is not None:
            self.fat_fract = m.get('FatFract')
        if m.get('LiverHU') is not None:
            self.liver_hu = m.get('LiverHU')
        if m.get('LiverROI1') is not None:
            self.liver_roi1 = m.get('LiverROI1')
        if m.get('LiverROI2') is not None:
            self.liver_roi2 = m.get('LiverROI2')
        if m.get('LiverROI3') is not None:
            self.liver_roi3 = m.get('LiverROI3')
        if m.get('LiverSlice') is not None:
            self.liver_slice = m.get('LiverSlice')
        if m.get('LiverSpleenDifference') is not None:
            self.liver_spleen_difference = m.get('LiverSpleenDifference')
        if m.get('LiverSpleenRatio') is not None:
            self.liver_spleen_ratio = m.get('LiverSpleenRatio')
        if m.get('LiverVolume') is not None:
            self.liver_volume = m.get('LiverVolume')
        if m.get('MaossScore') is not None:
            self.maoss_score = m.get('MaossScore')
        if m.get('Prediction') is not None:
            self.prediction = m.get('Prediction')
        if m.get('Probability') is not None:
            self.probability = m.get('Probability')
        if m.get('ROI1Center') is not None:
            self.roi1center = m.get('ROI1Center')
        if m.get('ROI2Center') is not None:
            self.roi2center = m.get('ROI2Center')
        if m.get('ROI3Center') is not None:
            self.roi3center = m.get('ROI3Center')
        if m.get('Radius') is not None:
            self.radius = m.get('Radius')
        if m.get('SpleenCenter') is not None:
            self.spleen_center = m.get('SpleenCenter')
        if m.get('SpleenHU') is not None:
            self.spleen_hu = m.get('SpleenHU')
        if m.get('SpleenROI') is not None:
            self.spleen_roi = m.get('SpleenROI')
        if m.get('SpleenSlice') is not None:
            self.spleen_slice = m.get('SpleenSlice')
        if m.get('SpleenVolume') is not None:
            self.spleen_volume = m.get('SpleenVolume')
        return self


class ScreenChestCTResponseBodyDataDetectLiverSteatosis(TeaModel):
    def __init__(
        self,
        detections: List[ScreenChestCTResponseBodyDataDetectLiverSteatosisDetections] = None,
        origin: List[float] = None,
        result_url: str = None,
        series_instance_uid: str = None,
        spacing: List[float] = None,
    ):
        self.detections = detections
        self.origin = origin
        self.result_url = result_url
        self.series_instance_uid = series_instance_uid
        self.spacing = spacing

    def validate(self):
        if self.detections:
            for k in self.detections:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Detections'] = []
        if self.detections is not None:
            for k in self.detections:
                result['Detections'].append(k.to_map() if k else None)
        if self.origin is not None:
            result['Origin'] = self.origin
        if self.result_url is not None:
            result['ResultUrl'] = self.result_url
        if self.series_instance_uid is not None:
            result['SeriesInstanceUid'] = self.series_instance_uid
        if self.spacing is not None:
            result['Spacing'] = self.spacing
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.detections = []
        if m.get('Detections') is not None:
            for k in m.get('Detections'):
                temp_model = ScreenChestCTResponseBodyDataDetectLiverSteatosisDetections()
                self.detections.append(temp_model.from_map(k))
        if m.get('Origin') is not None:
            self.origin = m.get('Origin')
        if m.get('ResultUrl') is not None:
            self.result_url = m.get('ResultUrl')
        if m.get('SeriesInstanceUid') is not None:
            self.series_instance_uid = m.get('SeriesInstanceUid')
        if m.get('Spacing') is not None:
            self.spacing = m.get('Spacing')
        return self


class ScreenChestCTResponseBodyDataDetectLymphLesions(TeaModel):
    def __init__(
        self,
        boxes: List[float] = None,
        diametermm: List[float] = None,
        key_slice: int = None,
        recist: List[List[float]] = None,
        score: float = None,
    ):
        self.boxes = boxes
        self.diametermm = diametermm
        self.key_slice = key_slice
        self.recist = recist
        self.score = score

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.boxes is not None:
            result['Boxes'] = self.boxes
        if self.diametermm is not None:
            result['Diametermm'] = self.diametermm
        if self.key_slice is not None:
            result['KeySlice'] = self.key_slice
        if self.recist is not None:
            result['Recist'] = self.recist
        if self.score is not None:
            result['Score'] = self.score
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Boxes') is not None:
            self.boxes = m.get('Boxes')
        if m.get('Diametermm') is not None:
            self.diametermm = m.get('Diametermm')
        if m.get('KeySlice') is not None:
            self.key_slice = m.get('KeySlice')
        if m.get('Recist') is not None:
            self.recist = m.get('Recist')
        if m.get('Score') is not None:
            self.score = m.get('Score')
        return self


class ScreenChestCTResponseBodyDataDetectLymph(TeaModel):
    def __init__(
        self,
        lesions: List[ScreenChestCTResponseBodyDataDetectLymphLesions] = None,
        series_instance_uid: str = None,
    ):
        self.lesions = lesions
        self.series_instance_uid = series_instance_uid

    def validate(self):
        if self.lesions:
            for k in self.lesions:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Lesions'] = []
        if self.lesions is not None:
            for k in self.lesions:
                result['Lesions'].append(k.to_map() if k else None)
        if self.series_instance_uid is not None:
            result['SeriesInstanceUID'] = self.series_instance_uid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.lesions = []
        if m.get('Lesions') is not None:
            for k in m.get('Lesions'):
                temp_model = ScreenChestCTResponseBodyDataDetectLymphLesions()
                self.lesions.append(temp_model.from_map(k))
        if m.get('SeriesInstanceUID') is not None:
            self.series_instance_uid = m.get('SeriesInstanceUID')
        return self


class ScreenChestCTResponseBodyDataDetectPdacLesionLesionList(TeaModel):
    def __init__(
        self,
        diameter: List[float] = None,
        key_slice: int = None,
        roiendpoints: List[List[int]] = None,
        recist_endpoints: List[List[int]] = None,
        type: str = None,
    ):
        self.diameter = diameter
        self.key_slice = key_slice
        self.roiendpoints = roiendpoints
        self.recist_endpoints = recist_endpoints
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.diameter is not None:
            result['Diameter'] = self.diameter
        if self.key_slice is not None:
            result['KeySlice'] = self.key_slice
        if self.roiendpoints is not None:
            result['ROIEndpoints'] = self.roiendpoints
        if self.recist_endpoints is not None:
            result['RecistEndpoints'] = self.recist_endpoints
        if self.type is not None:
            result['Type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Diameter') is not None:
            self.diameter = m.get('Diameter')
        if m.get('KeySlice') is not None:
            self.key_slice = m.get('KeySlice')
        if m.get('ROIEndpoints') is not None:
            self.roiendpoints = m.get('ROIEndpoints')
        if m.get('RecistEndpoints') is not None:
            self.recist_endpoints = m.get('RecistEndpoints')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        return self


class ScreenChestCTResponseBodyDataDetectPdacLesionOrganList(TeaModel):
    def __init__(
        self,
        diameter: List[float] = None,
        key_slice: int = None,
        roiendpoints: List[List[int]] = None,
        recist_endpoints: List[List[int]] = None,
        type: str = None,
    ):
        self.diameter = diameter
        self.key_slice = key_slice
        self.roiendpoints = roiendpoints
        self.recist_endpoints = recist_endpoints
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.diameter is not None:
            result['Diameter'] = self.diameter
        if self.key_slice is not None:
            result['KeySlice'] = self.key_slice
        if self.roiendpoints is not None:
            result['ROIEndpoints'] = self.roiendpoints
        if self.recist_endpoints is not None:
            result['RecistEndpoints'] = self.recist_endpoints
        if self.type is not None:
            result['Type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Diameter') is not None:
            self.diameter = m.get('Diameter')
        if m.get('KeySlice') is not None:
            self.key_slice = m.get('KeySlice')
        if m.get('ROIEndpoints') is not None:
            self.roiendpoints = m.get('ROIEndpoints')
        if m.get('RecistEndpoints') is not None:
            self.recist_endpoints = m.get('RecistEndpoints')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        return self


class ScreenChestCTResponseBodyDataDetectPdacLesion(TeaModel):
    def __init__(
        self,
        lesion_list: List[ScreenChestCTResponseBodyDataDetectPdacLesionLesionList] = None,
        mask: str = None,
        non_pdac_vol: str = None,
        organ_list: List[ScreenChestCTResponseBodyDataDetectPdacLesionOrganList] = None,
        panc_vol: str = None,
        pdac_vol: str = None,
        possibilities: List[str] = None,
    ):
        self.lesion_list = lesion_list
        self.mask = mask
        self.non_pdac_vol = non_pdac_vol
        self.organ_list = organ_list
        self.panc_vol = panc_vol
        self.pdac_vol = pdac_vol
        self.possibilities = possibilities

    def validate(self):
        if self.lesion_list:
            for k in self.lesion_list:
                if k:
                    k.validate()
        if self.organ_list:
            for k in self.organ_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['LesionList'] = []
        if self.lesion_list is not None:
            for k in self.lesion_list:
                result['LesionList'].append(k.to_map() if k else None)
        if self.mask is not None:
            result['Mask'] = self.mask
        if self.non_pdac_vol is not None:
            result['NonPdacVol'] = self.non_pdac_vol
        result['OrganList'] = []
        if self.organ_list is not None:
            for k in self.organ_list:
                result['OrganList'].append(k.to_map() if k else None)
        if self.panc_vol is not None:
            result['PancVol'] = self.panc_vol
        if self.pdac_vol is not None:
            result['PdacVol'] = self.pdac_vol
        if self.possibilities is not None:
            result['Possibilities'] = self.possibilities
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.lesion_list = []
        if m.get('LesionList') is not None:
            for k in m.get('LesionList'):
                temp_model = ScreenChestCTResponseBodyDataDetectPdacLesionLesionList()
                self.lesion_list.append(temp_model.from_map(k))
        if m.get('Mask') is not None:
            self.mask = m.get('Mask')
        if m.get('NonPdacVol') is not None:
            self.non_pdac_vol = m.get('NonPdacVol')
        self.organ_list = []
        if m.get('OrganList') is not None:
            for k in m.get('OrganList'):
                temp_model = ScreenChestCTResponseBodyDataDetectPdacLesionOrganList()
                self.organ_list.append(temp_model.from_map(k))
        if m.get('PancVol') is not None:
            self.panc_vol = m.get('PancVol')
        if m.get('PdacVol') is not None:
            self.pdac_vol = m.get('PdacVol')
        if m.get('Possibilities') is not None:
            self.possibilities = m.get('Possibilities')
        return self


class ScreenChestCTResponseBodyDataDetectPdac(TeaModel):
    def __init__(
        self,
        lesion: ScreenChestCTResponseBodyDataDetectPdacLesion = None,
        series_instance_uid: str = None,
    ):
        self.lesion = lesion
        self.series_instance_uid = series_instance_uid

    def validate(self):
        if self.lesion:
            self.lesion.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lesion is not None:
            result['Lesion'] = self.lesion.to_map()
        if self.series_instance_uid is not None:
            result['SeriesInstanceUID'] = self.series_instance_uid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lesion') is not None:
            temp_model = ScreenChestCTResponseBodyDataDetectPdacLesion()
            self.lesion = temp_model.from_map(m['Lesion'])
        if m.get('SeriesInstanceUID') is not None:
            self.series_instance_uid = m.get('SeriesInstanceUID')
        return self


class ScreenChestCTResponseBodyDataDetectRibFractureDetections(TeaModel):
    def __init__(
        self,
        coordinate_image: List[int] = None,
        coordinates: List[int] = None,
        frac_sopinstance_uid: str = None,
        fracture_category: int = None,
        fracture_confidence: float = None,
        fracture_id: int = None,
        fracture_location: str = None,
        fracture_segment: int = None,
    ):
        self.coordinate_image = coordinate_image
        self.coordinates = coordinates
        self.frac_sopinstance_uid = frac_sopinstance_uid
        self.fracture_category = fracture_category
        self.fracture_confidence = fracture_confidence
        self.fracture_id = fracture_id
        self.fracture_location = fracture_location
        self.fracture_segment = fracture_segment

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.coordinate_image is not None:
            result['CoordinateImage'] = self.coordinate_image
        if self.coordinates is not None:
            result['Coordinates'] = self.coordinates
        if self.frac_sopinstance_uid is not None:
            result['FracSOPInstanceUID'] = self.frac_sopinstance_uid
        if self.fracture_category is not None:
            result['FractureCategory'] = self.fracture_category
        if self.fracture_confidence is not None:
            result['FractureConfidence'] = self.fracture_confidence
        if self.fracture_id is not None:
            result['FractureId'] = self.fracture_id
        if self.fracture_location is not None:
            result['FractureLocation'] = self.fracture_location
        if self.fracture_segment is not None:
            result['FractureSegment'] = self.fracture_segment
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CoordinateImage') is not None:
            self.coordinate_image = m.get('CoordinateImage')
        if m.get('Coordinates') is not None:
            self.coordinates = m.get('Coordinates')
        if m.get('FracSOPInstanceUID') is not None:
            self.frac_sopinstance_uid = m.get('FracSOPInstanceUID')
        if m.get('FractureCategory') is not None:
            self.fracture_category = m.get('FractureCategory')
        if m.get('FractureConfidence') is not None:
            self.fracture_confidence = m.get('FractureConfidence')
        if m.get('FractureId') is not None:
            self.fracture_id = m.get('FractureId')
        if m.get('FractureLocation') is not None:
            self.fracture_location = m.get('FractureLocation')
        if m.get('FractureSegment') is not None:
            self.fracture_segment = m.get('FractureSegment')
        return self


class ScreenChestCTResponseBodyDataDetectRibFracture(TeaModel):
    def __init__(
        self,
        detections: List[ScreenChestCTResponseBodyDataDetectRibFractureDetections] = None,
        fracture_mask_url: str = None,
        origin: List[float] = None,
        result_url: str = None,
        rib_segment_mask_url: str = None,
        series_instance_uid: str = None,
        spacing: List[float] = None,
    ):
        self.detections = detections
        self.fracture_mask_url = fracture_mask_url
        self.origin = origin
        self.result_url = result_url
        self.rib_segment_mask_url = rib_segment_mask_url
        self.series_instance_uid = series_instance_uid
        self.spacing = spacing

    def validate(self):
        if self.detections:
            for k in self.detections:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Detections'] = []
        if self.detections is not None:
            for k in self.detections:
                result['Detections'].append(k.to_map() if k else None)
        if self.fracture_mask_url is not None:
            result['FractureMaskURL'] = self.fracture_mask_url
        if self.origin is not None:
            result['Origin'] = self.origin
        if self.result_url is not None:
            result['ResultURL'] = self.result_url
        if self.rib_segment_mask_url is not None:
            result['RibSegmentMaskURL'] = self.rib_segment_mask_url
        if self.series_instance_uid is not None:
            result['SeriesInstanceUID'] = self.series_instance_uid
        if self.spacing is not None:
            result['Spacing'] = self.spacing
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.detections = []
        if m.get('Detections') is not None:
            for k in m.get('Detections'):
                temp_model = ScreenChestCTResponseBodyDataDetectRibFractureDetections()
                self.detections.append(temp_model.from_map(k))
        if m.get('FractureMaskURL') is not None:
            self.fracture_mask_url = m.get('FractureMaskURL')
        if m.get('Origin') is not None:
            self.origin = m.get('Origin')
        if m.get('ResultURL') is not None:
            self.result_url = m.get('ResultURL')
        if m.get('RibSegmentMaskURL') is not None:
            self.rib_segment_mask_url = m.get('RibSegmentMaskURL')
        if m.get('SeriesInstanceUID') is not None:
            self.series_instance_uid = m.get('SeriesInstanceUID')
        if m.get('Spacing') is not None:
            self.spacing = m.get('Spacing')
        return self


class ScreenChestCTResponseBodyDataLungNoduleSeriesElements(TeaModel):
    def __init__(
        self,
        category: str = None,
        confidence: float = None,
        diameter: float = None,
        image_x: float = None,
        image_y: float = None,
        image_z: float = None,
        lobe: str = None,
        lung: str = None,
        major_axis: List[float] = None,
        mean_value: float = None,
        minor_axis: List[float] = None,
        recist_sopinstance_uid: str = None,
        risk: float = None,
        sopinstance_uid: str = None,
        volume: float = None,
        x: float = None,
        y: float = None,
        z: float = None,
    ):
        self.category = category
        self.confidence = confidence
        self.diameter = diameter
        self.image_x = image_x
        self.image_y = image_y
        self.image_z = image_z
        self.lobe = lobe
        self.lung = lung
        self.major_axis = major_axis
        self.mean_value = mean_value
        self.minor_axis = minor_axis
        self.recist_sopinstance_uid = recist_sopinstance_uid
        self.risk = risk
        self.sopinstance_uid = sopinstance_uid
        self.volume = volume
        self.x = x
        self.y = y
        self.z = z

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.category is not None:
            result['Category'] = self.category
        if self.confidence is not None:
            result['Confidence'] = self.confidence
        if self.diameter is not None:
            result['Diameter'] = self.diameter
        if self.image_x is not None:
            result['ImageX'] = self.image_x
        if self.image_y is not None:
            result['ImageY'] = self.image_y
        if self.image_z is not None:
            result['ImageZ'] = self.image_z
        if self.lobe is not None:
            result['Lobe'] = self.lobe
        if self.lung is not None:
            result['Lung'] = self.lung
        if self.major_axis is not None:
            result['MajorAxis'] = self.major_axis
        if self.mean_value is not None:
            result['MeanValue'] = self.mean_value
        if self.minor_axis is not None:
            result['MinorAxis'] = self.minor_axis
        if self.recist_sopinstance_uid is not None:
            result['RecistSOPInstanceUID'] = self.recist_sopinstance_uid
        if self.risk is not None:
            result['Risk'] = self.risk
        if self.sopinstance_uid is not None:
            result['SOPInstanceUID'] = self.sopinstance_uid
        if self.volume is not None:
            result['Volume'] = self.volume
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        if self.z is not None:
            result['Z'] = self.z
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Category') is not None:
            self.category = m.get('Category')
        if m.get('Confidence') is not None:
            self.confidence = m.get('Confidence')
        if m.get('Diameter') is not None:
            self.diameter = m.get('Diameter')
        if m.get('ImageX') is not None:
            self.image_x = m.get('ImageX')
        if m.get('ImageY') is not None:
            self.image_y = m.get('ImageY')
        if m.get('ImageZ') is not None:
            self.image_z = m.get('ImageZ')
        if m.get('Lobe') is not None:
            self.lobe = m.get('Lobe')
        if m.get('Lung') is not None:
            self.lung = m.get('Lung')
        if m.get('MajorAxis') is not None:
            self.major_axis = m.get('MajorAxis')
        if m.get('MeanValue') is not None:
            self.mean_value = m.get('MeanValue')
        if m.get('MinorAxis') is not None:
            self.minor_axis = m.get('MinorAxis')
        if m.get('RecistSOPInstanceUID') is not None:
            self.recist_sopinstance_uid = m.get('RecistSOPInstanceUID')
        if m.get('Risk') is not None:
            self.risk = m.get('Risk')
        if m.get('SOPInstanceUID') is not None:
            self.sopinstance_uid = m.get('SOPInstanceUID')
        if m.get('Volume') is not None:
            self.volume = m.get('Volume')
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('Z') is not None:
            self.z = m.get('Z')
        return self


class ScreenChestCTResponseBodyDataLungNoduleSeries(TeaModel):
    def __init__(
        self,
        elements: List[ScreenChestCTResponseBodyDataLungNoduleSeriesElements] = None,
        origin: List[float] = None,
        report: str = None,
        series_instance_uid: str = None,
        spacing: List[float] = None,
    ):
        self.elements = elements
        self.origin = origin
        self.report = report
        self.series_instance_uid = series_instance_uid
        self.spacing = spacing

    def validate(self):
        if self.elements:
            for k in self.elements:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Elements'] = []
        if self.elements is not None:
            for k in self.elements:
                result['Elements'].append(k.to_map() if k else None)
        if self.origin is not None:
            result['Origin'] = self.origin
        if self.report is not None:
            result['Report'] = self.report
        if self.series_instance_uid is not None:
            result['SeriesInstanceUid'] = self.series_instance_uid
        if self.spacing is not None:
            result['Spacing'] = self.spacing
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.elements = []
        if m.get('Elements') is not None:
            for k in m.get('Elements'):
                temp_model = ScreenChestCTResponseBodyDataLungNoduleSeriesElements()
                self.elements.append(temp_model.from_map(k))
        if m.get('Origin') is not None:
            self.origin = m.get('Origin')
        if m.get('Report') is not None:
            self.report = m.get('Report')
        if m.get('SeriesInstanceUid') is not None:
            self.series_instance_uid = m.get('SeriesInstanceUid')
        if m.get('Spacing') is not None:
            self.spacing = m.get('Spacing')
        return self


class ScreenChestCTResponseBodyDataLungNodule(TeaModel):
    def __init__(
        self,
        series: List[ScreenChestCTResponseBodyDataLungNoduleSeries] = None,
    ):
        self.series = series

    def validate(self):
        if self.series:
            for k in self.series:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Series'] = []
        if self.series is not None:
            for k in self.series:
                result['Series'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.series = []
        if m.get('Series') is not None:
            for k in m.get('Series'):
                temp_model = ScreenChestCTResponseBodyDataLungNoduleSeries()
                self.series.append(temp_model.from_map(k))
        return self


class ScreenChestCTResponseBodyDataMuscleFat(TeaModel):
    def __init__(
        self,
        fat__type: int = None,
        mask__path: str = None,
        muscle__mass: int = None,
        muscle__quality: int = None,
        nama__tama__index__tscore: float = None,
        percent__imat: float = None,
        percent__lama: float = None,
        percent__nama: float = None,
        rendering__path: str = None,
        sfa: float = None,
        sft: float = None,
        sma: float = None,
        smi: float = None,
        study__age: int = None,
        study__gender: str = None,
        series_instance_uid: str = None,
        vertebra__in__use: float = None,
        vfa: float = None,
    ):
        self.fat__type = fat__type
        self.mask__path = mask__path
        self.muscle__mass = muscle__mass
        self.muscle__quality = muscle__quality
        self.nama__tama__index__tscore = nama__tama__index__tscore
        self.percent__imat = percent__imat
        self.percent__lama = percent__lama
        self.percent__nama = percent__nama
        self.rendering__path = rendering__path
        self.sfa = sfa
        self.sft = sft
        self.sma = sma
        self.smi = smi
        self.study__age = study__age
        self.study__gender = study__gender
        self.series_instance_uid = series_instance_uid
        self.vertebra__in__use = vertebra__in__use
        self.vfa = vfa

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.fat__type is not None:
            result['FAT_TYPE'] = self.fat__type
        if self.mask__path is not None:
            result['MASK_PATH'] = self.mask__path
        if self.muscle__mass is not None:
            result['MUSCLE_MASS'] = self.muscle__mass
        if self.muscle__quality is not None:
            result['MUSCLE_QUALITY'] = self.muscle__quality
        if self.nama__tama__index__tscore is not None:
            result['NAMA_TAMA_INDEX_TSCORE'] = self.nama__tama__index__tscore
        if self.percent__imat is not None:
            result['PERCENT_IMAT'] = self.percent__imat
        if self.percent__lama is not None:
            result['PERCENT_LAMA'] = self.percent__lama
        if self.percent__nama is not None:
            result['PERCENT_NAMA'] = self.percent__nama
        if self.rendering__path is not None:
            result['RENDERING_PATH'] = self.rendering__path
        if self.sfa is not None:
            result['SFA'] = self.sfa
        if self.sft is not None:
            result['SFT'] = self.sft
        if self.sma is not None:
            result['SMA'] = self.sma
        if self.smi is not None:
            result['SMI'] = self.smi
        if self.study__age is not None:
            result['STUDY_AGE'] = self.study__age
        if self.study__gender is not None:
            result['STUDY_GENDER'] = self.study__gender
        if self.series_instance_uid is not None:
            result['SeriesInstanceUid'] = self.series_instance_uid
        if self.vertebra__in__use is not None:
            result['VERTEBRA_IN_USE'] = self.vertebra__in__use
        if self.vfa is not None:
            result['VFA'] = self.vfa
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FAT_TYPE') is not None:
            self.fat__type = m.get('FAT_TYPE')
        if m.get('MASK_PATH') is not None:
            self.mask__path = m.get('MASK_PATH')
        if m.get('MUSCLE_MASS') is not None:
            self.muscle__mass = m.get('MUSCLE_MASS')
        if m.get('MUSCLE_QUALITY') is not None:
            self.muscle__quality = m.get('MUSCLE_QUALITY')
        if m.get('NAMA_TAMA_INDEX_TSCORE') is not None:
            self.nama__tama__index__tscore = m.get('NAMA_TAMA_INDEX_TSCORE')
        if m.get('PERCENT_IMAT') is not None:
            self.percent__imat = m.get('PERCENT_IMAT')
        if m.get('PERCENT_LAMA') is not None:
            self.percent__lama = m.get('PERCENT_LAMA')
        if m.get('PERCENT_NAMA') is not None:
            self.percent__nama = m.get('PERCENT_NAMA')
        if m.get('RENDERING_PATH') is not None:
            self.rendering__path = m.get('RENDERING_PATH')
        if m.get('SFA') is not None:
            self.sfa = m.get('SFA')
        if m.get('SFT') is not None:
            self.sft = m.get('SFT')
        if m.get('SMA') is not None:
            self.sma = m.get('SMA')
        if m.get('SMI') is not None:
            self.smi = m.get('SMI')
        if m.get('STUDY_AGE') is not None:
            self.study__age = m.get('STUDY_AGE')
        if m.get('STUDY_GENDER') is not None:
            self.study__gender = m.get('STUDY_GENDER')
        if m.get('SeriesInstanceUid') is not None:
            self.series_instance_uid = m.get('SeriesInstanceUid')
        if m.get('VERTEBRA_IN_USE') is not None:
            self.vertebra__in__use = m.get('VERTEBRA_IN_USE')
        if m.get('VFA') is not None:
            self.vfa = m.get('VFA')
        return self


class ScreenChestCTResponseBodyDataPredictCVDLesionFeatureScore(TeaModel):
    def __init__(
        self,
        aorta_calcium_score: List[float] = None,
        aorta_calcium_volume: List[float] = None,
        aorta_max_diam: List[float] = None,
        aorta_max_diam_std: List[float] = None,
        aortic_height_index: List[float] = None,
        aortic_tortuosity_index: List[float] = None,
        asc_ao_max_diam: List[float] = None,
        ascend_aorta_length: List[float] = None,
        cardio_thoracic_ratio: List[float] = None,
        chest_width: List[float] = None,
        coronary_calcium_score: List[float] = None,
        coronary_calcium_vol: List[float] = None,
        deep_feature: List[float] = None,
        eat_humean: List[float] = None,
        eat_hustd: List[float] = None,
        eat_volume: List[float] = None,
        heart_long_diam: List[float] = None,
        heart_short_diam: List[float] = None,
        heart_width: List[float] = None,
        left_lung_highatt_ratio: List[float] = None,
        left_lung_lowatt_ratio: List[float] = None,
        myo_epi_ratio: List[float] = None,
        right_lung_highatt_ratio: List[float] = None,
        right_lung_lowatt_ratio: List[float] = None,
    ):
        self.aorta_calcium_score = aorta_calcium_score
        self.aorta_calcium_volume = aorta_calcium_volume
        self.aorta_max_diam = aorta_max_diam
        self.aorta_max_diam_std = aorta_max_diam_std
        self.aortic_height_index = aortic_height_index
        self.aortic_tortuosity_index = aortic_tortuosity_index
        self.asc_ao_max_diam = asc_ao_max_diam
        self.ascend_aorta_length = ascend_aorta_length
        self.cardio_thoracic_ratio = cardio_thoracic_ratio
        self.chest_width = chest_width
        self.coronary_calcium_score = coronary_calcium_score
        self.coronary_calcium_vol = coronary_calcium_vol
        self.deep_feature = deep_feature
        self.eat_humean = eat_humean
        self.eat_hustd = eat_hustd
        self.eat_volume = eat_volume
        self.heart_long_diam = heart_long_diam
        self.heart_short_diam = heart_short_diam
        self.heart_width = heart_width
        self.left_lung_highatt_ratio = left_lung_highatt_ratio
        self.left_lung_lowatt_ratio = left_lung_lowatt_ratio
        self.myo_epi_ratio = myo_epi_ratio
        self.right_lung_highatt_ratio = right_lung_highatt_ratio
        self.right_lung_lowatt_ratio = right_lung_lowatt_ratio

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.aorta_calcium_score is not None:
            result['AortaCalciumScore'] = self.aorta_calcium_score
        if self.aorta_calcium_volume is not None:
            result['AortaCalciumVolume'] = self.aorta_calcium_volume
        if self.aorta_max_diam is not None:
            result['AortaMaxDiam'] = self.aorta_max_diam
        if self.aorta_max_diam_std is not None:
            result['AortaMaxDiamStd'] = self.aorta_max_diam_std
        if self.aortic_height_index is not None:
            result['AorticHeightIndex'] = self.aortic_height_index
        if self.aortic_tortuosity_index is not None:
            result['AorticTortuosityIndex'] = self.aortic_tortuosity_index
        if self.asc_ao_max_diam is not None:
            result['AscAoMaxDiam'] = self.asc_ao_max_diam
        if self.ascend_aorta_length is not None:
            result['AscendAortaLength'] = self.ascend_aorta_length
        if self.cardio_thoracic_ratio is not None:
            result['CardioThoracicRatio'] = self.cardio_thoracic_ratio
        if self.chest_width is not None:
            result['ChestWidth'] = self.chest_width
        if self.coronary_calcium_score is not None:
            result['CoronaryCalciumScore'] = self.coronary_calcium_score
        if self.coronary_calcium_vol is not None:
            result['CoronaryCalciumVol'] = self.coronary_calcium_vol
        if self.deep_feature is not None:
            result['DeepFeature'] = self.deep_feature
        if self.eat_humean is not None:
            result['EatHUMean'] = self.eat_humean
        if self.eat_hustd is not None:
            result['EatHUSTD'] = self.eat_hustd
        if self.eat_volume is not None:
            result['EatVolume'] = self.eat_volume
        if self.heart_long_diam is not None:
            result['HeartLongDiam'] = self.heart_long_diam
        if self.heart_short_diam is not None:
            result['HeartShortDiam'] = self.heart_short_diam
        if self.heart_width is not None:
            result['HeartWidth'] = self.heart_width
        if self.left_lung_highatt_ratio is not None:
            result['LeftLungHighattRatio'] = self.left_lung_highatt_ratio
        if self.left_lung_lowatt_ratio is not None:
            result['LeftLungLowattRatio'] = self.left_lung_lowatt_ratio
        if self.myo_epi_ratio is not None:
            result['MyoEpiRatio'] = self.myo_epi_ratio
        if self.right_lung_highatt_ratio is not None:
            result['RightLungHighattRatio'] = self.right_lung_highatt_ratio
        if self.right_lung_lowatt_ratio is not None:
            result['RightLungLowattRatio'] = self.right_lung_lowatt_ratio
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AortaCalciumScore') is not None:
            self.aorta_calcium_score = m.get('AortaCalciumScore')
        if m.get('AortaCalciumVolume') is not None:
            self.aorta_calcium_volume = m.get('AortaCalciumVolume')
        if m.get('AortaMaxDiam') is not None:
            self.aorta_max_diam = m.get('AortaMaxDiam')
        if m.get('AortaMaxDiamStd') is not None:
            self.aorta_max_diam_std = m.get('AortaMaxDiamStd')
        if m.get('AorticHeightIndex') is not None:
            self.aortic_height_index = m.get('AorticHeightIndex')
        if m.get('AorticTortuosityIndex') is not None:
            self.aortic_tortuosity_index = m.get('AorticTortuosityIndex')
        if m.get('AscAoMaxDiam') is not None:
            self.asc_ao_max_diam = m.get('AscAoMaxDiam')
        if m.get('AscendAortaLength') is not None:
            self.ascend_aorta_length = m.get('AscendAortaLength')
        if m.get('CardioThoracicRatio') is not None:
            self.cardio_thoracic_ratio = m.get('CardioThoracicRatio')
        if m.get('ChestWidth') is not None:
            self.chest_width = m.get('ChestWidth')
        if m.get('CoronaryCalciumScore') is not None:
            self.coronary_calcium_score = m.get('CoronaryCalciumScore')
        if m.get('CoronaryCalciumVol') is not None:
            self.coronary_calcium_vol = m.get('CoronaryCalciumVol')
        if m.get('DeepFeature') is not None:
            self.deep_feature = m.get('DeepFeature')
        if m.get('EatHUMean') is not None:
            self.eat_humean = m.get('EatHUMean')
        if m.get('EatHUSTD') is not None:
            self.eat_hustd = m.get('EatHUSTD')
        if m.get('EatVolume') is not None:
            self.eat_volume = m.get('EatVolume')
        if m.get('HeartLongDiam') is not None:
            self.heart_long_diam = m.get('HeartLongDiam')
        if m.get('HeartShortDiam') is not None:
            self.heart_short_diam = m.get('HeartShortDiam')
        if m.get('HeartWidth') is not None:
            self.heart_width = m.get('HeartWidth')
        if m.get('LeftLungHighattRatio') is not None:
            self.left_lung_highatt_ratio = m.get('LeftLungHighattRatio')
        if m.get('LeftLungLowattRatio') is not None:
            self.left_lung_lowatt_ratio = m.get('LeftLungLowattRatio')
        if m.get('MyoEpiRatio') is not None:
            self.myo_epi_ratio = m.get('MyoEpiRatio')
        if m.get('RightLungHighattRatio') is not None:
            self.right_lung_highatt_ratio = m.get('RightLungHighattRatio')
        if m.get('RightLungLowattRatio') is not None:
            self.right_lung_lowatt_ratio = m.get('RightLungLowattRatio')
        return self


class ScreenChestCTResponseBodyDataPredictCVDLesion(TeaModel):
    def __init__(
        self,
        cvdprobability: float = None,
        feature_score: ScreenChestCTResponseBodyDataPredictCVDLesionFeatureScore = None,
        images_url: str = None,
        result_url: List[str] = None,
    ):
        self.cvdprobability = cvdprobability
        self.feature_score = feature_score
        self.images_url = images_url
        self.result_url = result_url

    def validate(self):
        if self.feature_score:
            self.feature_score.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cvdprobability is not None:
            result['CVDProbability'] = self.cvdprobability
        if self.feature_score is not None:
            result['FeatureScore'] = self.feature_score.to_map()
        if self.images_url is not None:
            result['ImagesURL'] = self.images_url
        if self.result_url is not None:
            result['ResultURL'] = self.result_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CVDProbability') is not None:
            self.cvdprobability = m.get('CVDProbability')
        if m.get('FeatureScore') is not None:
            temp_model = ScreenChestCTResponseBodyDataPredictCVDLesionFeatureScore()
            self.feature_score = temp_model.from_map(m['FeatureScore'])
        if m.get('ImagesURL') is not None:
            self.images_url = m.get('ImagesURL')
        if m.get('ResultURL') is not None:
            self.result_url = m.get('ResultURL')
        return self


class ScreenChestCTResponseBodyDataPredictCVD(TeaModel):
    def __init__(
        self,
        lesion: ScreenChestCTResponseBodyDataPredictCVDLesion = None,
        series_instance_uid: str = None,
    ):
        self.lesion = lesion
        self.series_instance_uid = series_instance_uid

    def validate(self):
        if self.lesion:
            self.lesion.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lesion is not None:
            result['Lesion'] = self.lesion.to_map()
        if self.series_instance_uid is not None:
            result['SeriesInstanceUid'] = self.series_instance_uid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lesion') is not None:
            temp_model = ScreenChestCTResponseBodyDataPredictCVDLesion()
            self.lesion = temp_model.from_map(m['Lesion'])
        if m.get('SeriesInstanceUid') is not None:
            self.series_instance_uid = m.get('SeriesInstanceUid')
        return self


class ScreenChestCTResponseBodyDataScreenBCLesionLeft(TeaModel):
    def __init__(
        self,
        bcvolume: str = None,
        breast_volume: str = None,
        probabilities: List[str] = None,
    ):
        self.bcvolume = bcvolume
        self.breast_volume = breast_volume
        self.probabilities = probabilities

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.bcvolume is not None:
            result['BCVolume'] = self.bcvolume
        if self.breast_volume is not None:
            result['BreastVolume'] = self.breast_volume
        if self.probabilities is not None:
            result['Probabilities'] = self.probabilities
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BCVolume') is not None:
            self.bcvolume = m.get('BCVolume')
        if m.get('BreastVolume') is not None:
            self.breast_volume = m.get('BreastVolume')
        if m.get('Probabilities') is not None:
            self.probabilities = m.get('Probabilities')
        return self


class ScreenChestCTResponseBodyDataScreenBCLesionLesionList(TeaModel):
    def __init__(
        self,
        diameter: List[float] = None,
        key_slice: int = None,
        roiendpoints: List[List[int]] = None,
        recist_endpoints: List[List[int]] = None,
        type: str = None,
    ):
        self.diameter = diameter
        self.key_slice = key_slice
        self.roiendpoints = roiendpoints
        self.recist_endpoints = recist_endpoints
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.diameter is not None:
            result['Diameter'] = self.diameter
        if self.key_slice is not None:
            result['KeySlice'] = self.key_slice
        if self.roiendpoints is not None:
            result['ROIEndpoints'] = self.roiendpoints
        if self.recist_endpoints is not None:
            result['RecistEndpoints'] = self.recist_endpoints
        if self.type is not None:
            result['Type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Diameter') is not None:
            self.diameter = m.get('Diameter')
        if m.get('KeySlice') is not None:
            self.key_slice = m.get('KeySlice')
        if m.get('ROIEndpoints') is not None:
            self.roiendpoints = m.get('ROIEndpoints')
        if m.get('RecistEndpoints') is not None:
            self.recist_endpoints = m.get('RecistEndpoints')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        return self


class ScreenChestCTResponseBodyDataScreenBCLesionOrganList(TeaModel):
    def __init__(
        self,
        diameter: List[float] = None,
        key_slice: int = None,
        roiendpoints: List[List[int]] = None,
        recist_endpoints: List[List[int]] = None,
        type: str = None,
    ):
        self.diameter = diameter
        self.key_slice = key_slice
        self.roiendpoints = roiendpoints
        self.recist_endpoints = recist_endpoints
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.diameter is not None:
            result['Diameter'] = self.diameter
        if self.key_slice is not None:
            result['KeySlice'] = self.key_slice
        if self.roiendpoints is not None:
            result['ROIEndpoints'] = self.roiendpoints
        if self.recist_endpoints is not None:
            result['RecistEndpoints'] = self.recist_endpoints
        if self.type is not None:
            result['Type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Diameter') is not None:
            self.diameter = m.get('Diameter')
        if m.get('KeySlice') is not None:
            self.key_slice = m.get('KeySlice')
        if m.get('ROIEndpoints') is not None:
            self.roiendpoints = m.get('ROIEndpoints')
        if m.get('RecistEndpoints') is not None:
            self.recist_endpoints = m.get('RecistEndpoints')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        return self


class ScreenChestCTResponseBodyDataScreenBCLesionRight(TeaModel):
    def __init__(
        self,
        bcvolume: str = None,
        breast_volume: str = None,
        probabilities: List[str] = None,
    ):
        self.bcvolume = bcvolume
        self.breast_volume = breast_volume
        self.probabilities = probabilities

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.bcvolume is not None:
            result['BCVolume'] = self.bcvolume
        if self.breast_volume is not None:
            result['BreastVolume'] = self.breast_volume
        if self.probabilities is not None:
            result['Probabilities'] = self.probabilities
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BCVolume') is not None:
            self.bcvolume = m.get('BCVolume')
        if m.get('BreastVolume') is not None:
            self.breast_volume = m.get('BreastVolume')
        if m.get('Probabilities') is not None:
            self.probabilities = m.get('Probabilities')
        return self


class ScreenChestCTResponseBodyDataScreenBCLesion(TeaModel):
    def __init__(
        self,
        left: ScreenChestCTResponseBodyDataScreenBCLesionLeft = None,
        lesion_list: List[ScreenChestCTResponseBodyDataScreenBCLesionLesionList] = None,
        mask: str = None,
        organ_list: List[ScreenChestCTResponseBodyDataScreenBCLesionOrganList] = None,
        right: ScreenChestCTResponseBodyDataScreenBCLesionRight = None,
    ):
        self.left = left
        self.lesion_list = lesion_list
        self.mask = mask
        self.organ_list = organ_list
        self.right = right

    def validate(self):
        if self.left:
            self.left.validate()
        if self.lesion_list:
            for k in self.lesion_list:
                if k:
                    k.validate()
        if self.organ_list:
            for k in self.organ_list:
                if k:
                    k.validate()
        if self.right:
            self.right.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.left is not None:
            result['Left'] = self.left.to_map()
        result['LesionList'] = []
        if self.lesion_list is not None:
            for k in self.lesion_list:
                result['LesionList'].append(k.to_map() if k else None)
        if self.mask is not None:
            result['Mask'] = self.mask
        result['OrganList'] = []
        if self.organ_list is not None:
            for k in self.organ_list:
                result['OrganList'].append(k.to_map() if k else None)
        if self.right is not None:
            result['Right'] = self.right.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Left') is not None:
            temp_model = ScreenChestCTResponseBodyDataScreenBCLesionLeft()
            self.left = temp_model.from_map(m['Left'])
        self.lesion_list = []
        if m.get('LesionList') is not None:
            for k in m.get('LesionList'):
                temp_model = ScreenChestCTResponseBodyDataScreenBCLesionLesionList()
                self.lesion_list.append(temp_model.from_map(k))
        if m.get('Mask') is not None:
            self.mask = m.get('Mask')
        self.organ_list = []
        if m.get('OrganList') is not None:
            for k in m.get('OrganList'):
                temp_model = ScreenChestCTResponseBodyDataScreenBCLesionOrganList()
                self.organ_list.append(temp_model.from_map(k))
        if m.get('Right') is not None:
            temp_model = ScreenChestCTResponseBodyDataScreenBCLesionRight()
            self.right = temp_model.from_map(m['Right'])
        return self


class ScreenChestCTResponseBodyDataScreenBC(TeaModel):
    def __init__(
        self,
        lesion: ScreenChestCTResponseBodyDataScreenBCLesion = None,
        series_instance_uid: str = None,
    ):
        self.lesion = lesion
        self.series_instance_uid = series_instance_uid

    def validate(self):
        if self.lesion:
            self.lesion.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lesion is not None:
            result['Lesion'] = self.lesion.to_map()
        if self.series_instance_uid is not None:
            result['SeriesInstanceUid'] = self.series_instance_uid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lesion') is not None:
            temp_model = ScreenChestCTResponseBodyDataScreenBCLesion()
            self.lesion = temp_model.from_map(m['Lesion'])
        if m.get('SeriesInstanceUid') is not None:
            self.series_instance_uid = m.get('SeriesInstanceUid')
        return self


class ScreenChestCTResponseBodyDataScreenCRCLesionLesionList(TeaModel):
    def __init__(
        self,
        diameter: List[float] = None,
        key_slice: int = None,
        roiendpoints: List[List[int]] = None,
        recist_endpoints: List[List[int]] = None,
        type: str = None,
    ):
        self.diameter = diameter
        self.key_slice = key_slice
        self.roiendpoints = roiendpoints
        self.recist_endpoints = recist_endpoints
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.diameter is not None:
            result['Diameter'] = self.diameter
        if self.key_slice is not None:
            result['KeySlice'] = self.key_slice
        if self.roiendpoints is not None:
            result['ROIEndpoints'] = self.roiendpoints
        if self.recist_endpoints is not None:
            result['RecistEndpoints'] = self.recist_endpoints
        if self.type is not None:
            result['Type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Diameter') is not None:
            self.diameter = m.get('Diameter')
        if m.get('KeySlice') is not None:
            self.key_slice = m.get('KeySlice')
        if m.get('ROIEndpoints') is not None:
            self.roiendpoints = m.get('ROIEndpoints')
        if m.get('RecistEndpoints') is not None:
            self.recist_endpoints = m.get('RecistEndpoints')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        return self


class ScreenChestCTResponseBodyDataScreenCRCLesionOrganList(TeaModel):
    def __init__(
        self,
        diameter: List[float] = None,
        key_slice: int = None,
        roiendpoints: List[List[int]] = None,
        recist_endpoints: List[List[int]] = None,
        type: str = None,
    ):
        self.diameter = diameter
        self.key_slice = key_slice
        self.roiendpoints = roiendpoints
        self.recist_endpoints = recist_endpoints
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.diameter is not None:
            result['Diameter'] = self.diameter
        if self.key_slice is not None:
            result['KeySlice'] = self.key_slice
        if self.roiendpoints is not None:
            result['ROIEndpoints'] = self.roiendpoints
        if self.recist_endpoints is not None:
            result['RecistEndpoints'] = self.recist_endpoints
        if self.type is not None:
            result['Type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Diameter') is not None:
            self.diameter = m.get('Diameter')
        if m.get('KeySlice') is not None:
            self.key_slice = m.get('KeySlice')
        if m.get('ROIEndpoints') is not None:
            self.roiendpoints = m.get('ROIEndpoints')
        if m.get('RecistEndpoints') is not None:
            self.recist_endpoints = m.get('RecistEndpoints')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        return self


class ScreenChestCTResponseBodyDataScreenCRCLesion(TeaModel):
    def __init__(
        self,
        colorectum_volume: str = None,
        lesion_list: List[ScreenChestCTResponseBodyDataScreenCRCLesionLesionList] = None,
        mask: str = None,
        organ_list: List[ScreenChestCTResponseBodyDataScreenCRCLesionOrganList] = None,
        probabilities: List[str] = None,
    ):
        self.colorectum_volume = colorectum_volume
        self.lesion_list = lesion_list
        self.mask = mask
        self.organ_list = organ_list
        self.probabilities = probabilities

    def validate(self):
        if self.lesion_list:
            for k in self.lesion_list:
                if k:
                    k.validate()
        if self.organ_list:
            for k in self.organ_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.colorectum_volume is not None:
            result['ColorectumVolume'] = self.colorectum_volume
        result['LesionList'] = []
        if self.lesion_list is not None:
            for k in self.lesion_list:
                result['LesionList'].append(k.to_map() if k else None)
        if self.mask is not None:
            result['Mask'] = self.mask
        result['OrganList'] = []
        if self.organ_list is not None:
            for k in self.organ_list:
                result['OrganList'].append(k.to_map() if k else None)
        if self.probabilities is not None:
            result['Probabilities'] = self.probabilities
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ColorectumVolume') is not None:
            self.colorectum_volume = m.get('ColorectumVolume')
        self.lesion_list = []
        if m.get('LesionList') is not None:
            for k in m.get('LesionList'):
                temp_model = ScreenChestCTResponseBodyDataScreenCRCLesionLesionList()
                self.lesion_list.append(temp_model.from_map(k))
        if m.get('Mask') is not None:
            self.mask = m.get('Mask')
        self.organ_list = []
        if m.get('OrganList') is not None:
            for k in m.get('OrganList'):
                temp_model = ScreenChestCTResponseBodyDataScreenCRCLesionOrganList()
                self.organ_list.append(temp_model.from_map(k))
        if m.get('Probabilities') is not None:
            self.probabilities = m.get('Probabilities')
        return self


class ScreenChestCTResponseBodyDataScreenCRC(TeaModel):
    def __init__(
        self,
        lesion: ScreenChestCTResponseBodyDataScreenCRCLesion = None,
        series_instance_uid: str = None,
    ):
        self.lesion = lesion
        self.series_instance_uid = series_instance_uid

    def validate(self):
        if self.lesion:
            self.lesion.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lesion is not None:
            result['Lesion'] = self.lesion.to_map()
        if self.series_instance_uid is not None:
            result['SeriesInstanceUid'] = self.series_instance_uid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lesion') is not None:
            temp_model = ScreenChestCTResponseBodyDataScreenCRCLesion()
            self.lesion = temp_model.from_map(m['Lesion'])
        if m.get('SeriesInstanceUid') is not None:
            self.series_instance_uid = m.get('SeriesInstanceUid')
        return self


class ScreenChestCTResponseBodyDataScreenEcLesionLesionList(TeaModel):
    def __init__(
        self,
        diameter: List[float] = None,
        key_slice: int = None,
        roiendpoints: List[List[int]] = None,
        recist_endpoints: List[List[int]] = None,
        type: str = None,
    ):
        self.diameter = diameter
        self.key_slice = key_slice
        self.roiendpoints = roiendpoints
        self.recist_endpoints = recist_endpoints
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.diameter is not None:
            result['Diameter'] = self.diameter
        if self.key_slice is not None:
            result['KeySlice'] = self.key_slice
        if self.roiendpoints is not None:
            result['ROIEndpoints'] = self.roiendpoints
        if self.recist_endpoints is not None:
            result['RecistEndpoints'] = self.recist_endpoints
        if self.type is not None:
            result['Type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Diameter') is not None:
            self.diameter = m.get('Diameter')
        if m.get('KeySlice') is not None:
            self.key_slice = m.get('KeySlice')
        if m.get('ROIEndpoints') is not None:
            self.roiendpoints = m.get('ROIEndpoints')
        if m.get('RecistEndpoints') is not None:
            self.recist_endpoints = m.get('RecistEndpoints')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        return self


class ScreenChestCTResponseBodyDataScreenEcLesionOrganList(TeaModel):
    def __init__(
        self,
        diameter: List[float] = None,
        key_slice: int = None,
        roiendpoints: List[List[int]] = None,
        recist_endpoints: List[List[int]] = None,
        type: str = None,
    ):
        self.diameter = diameter
        self.key_slice = key_slice
        self.roiendpoints = roiendpoints
        self.recist_endpoints = recist_endpoints
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.diameter is not None:
            result['Diameter'] = self.diameter
        if self.key_slice is not None:
            result['KeySlice'] = self.key_slice
        if self.roiendpoints is not None:
            result['ROIEndpoints'] = self.roiendpoints
        if self.recist_endpoints is not None:
            result['RecistEndpoints'] = self.recist_endpoints
        if self.type is not None:
            result['Type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Diameter') is not None:
            self.diameter = m.get('Diameter')
        if m.get('KeySlice') is not None:
            self.key_slice = m.get('KeySlice')
        if m.get('ROIEndpoints') is not None:
            self.roiendpoints = m.get('ROIEndpoints')
        if m.get('RecistEndpoints') is not None:
            self.recist_endpoints = m.get('RecistEndpoints')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        return self


class ScreenChestCTResponseBodyDataScreenEcLesion(TeaModel):
    def __init__(
        self,
        benign_volume: str = None,
        ec_volume: str = None,
        egj_volume: str = None,
        eso_volume: str = None,
        lesion_list: List[ScreenChestCTResponseBodyDataScreenEcLesionLesionList] = None,
        mask: str = None,
        organ_list: List[ScreenChestCTResponseBodyDataScreenEcLesionOrganList] = None,
        possibilities: List[str] = None,
    ):
        self.benign_volume = benign_volume
        self.ec_volume = ec_volume
        self.egj_volume = egj_volume
        self.eso_volume = eso_volume
        self.lesion_list = lesion_list
        self.mask = mask
        self.organ_list = organ_list
        self.possibilities = possibilities

    def validate(self):
        if self.lesion_list:
            for k in self.lesion_list:
                if k:
                    k.validate()
        if self.organ_list:
            for k in self.organ_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.benign_volume is not None:
            result['BenignVolume'] = self.benign_volume
        if self.ec_volume is not None:
            result['EcVolume'] = self.ec_volume
        if self.egj_volume is not None:
            result['EgjVolume'] = self.egj_volume
        if self.eso_volume is not None:
            result['EsoVolume'] = self.eso_volume
        result['LesionList'] = []
        if self.lesion_list is not None:
            for k in self.lesion_list:
                result['LesionList'].append(k.to_map() if k else None)
        if self.mask is not None:
            result['Mask'] = self.mask
        result['OrganList'] = []
        if self.organ_list is not None:
            for k in self.organ_list:
                result['OrganList'].append(k.to_map() if k else None)
        if self.possibilities is not None:
            result['Possibilities'] = self.possibilities
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BenignVolume') is not None:
            self.benign_volume = m.get('BenignVolume')
        if m.get('EcVolume') is not None:
            self.ec_volume = m.get('EcVolume')
        if m.get('EgjVolume') is not None:
            self.egj_volume = m.get('EgjVolume')
        if m.get('EsoVolume') is not None:
            self.eso_volume = m.get('EsoVolume')
        self.lesion_list = []
        if m.get('LesionList') is not None:
            for k in m.get('LesionList'):
                temp_model = ScreenChestCTResponseBodyDataScreenEcLesionLesionList()
                self.lesion_list.append(temp_model.from_map(k))
        if m.get('Mask') is not None:
            self.mask = m.get('Mask')
        self.organ_list = []
        if m.get('OrganList') is not None:
            for k in m.get('OrganList'):
                temp_model = ScreenChestCTResponseBodyDataScreenEcLesionOrganList()
                self.organ_list.append(temp_model.from_map(k))
        if m.get('Possibilities') is not None:
            self.possibilities = m.get('Possibilities')
        return self


class ScreenChestCTResponseBodyDataScreenEc(TeaModel):
    def __init__(
        self,
        lesion: ScreenChestCTResponseBodyDataScreenEcLesion = None,
        series_instance_uid: str = None,
    ):
        self.lesion = lesion
        self.series_instance_uid = series_instance_uid

    def validate(self):
        if self.lesion:
            self.lesion.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lesion is not None:
            result['Lesion'] = self.lesion.to_map()
        if self.series_instance_uid is not None:
            result['SeriesInstanceUid'] = self.series_instance_uid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lesion') is not None:
            temp_model = ScreenChestCTResponseBodyDataScreenEcLesion()
            self.lesion = temp_model.from_map(m['Lesion'])
        if m.get('SeriesInstanceUid') is not None:
            self.series_instance_uid = m.get('SeriesInstanceUid')
        return self


class ScreenChestCTResponseBodyDataScreenGCLesionLesionList(TeaModel):
    def __init__(
        self,
        diameter: List[float] = None,
        key_slice: int = None,
        roiendpoints: List[List[int]] = None,
        recist_endpoints: List[List[int]] = None,
        type: str = None,
    ):
        self.diameter = diameter
        self.key_slice = key_slice
        self.roiendpoints = roiendpoints
        self.recist_endpoints = recist_endpoints
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.diameter is not None:
            result['Diameter'] = self.diameter
        if self.key_slice is not None:
            result['KeySlice'] = self.key_slice
        if self.roiendpoints is not None:
            result['ROIEndpoints'] = self.roiendpoints
        if self.recist_endpoints is not None:
            result['RecistEndpoints'] = self.recist_endpoints
        if self.type is not None:
            result['Type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Diameter') is not None:
            self.diameter = m.get('Diameter')
        if m.get('KeySlice') is not None:
            self.key_slice = m.get('KeySlice')
        if m.get('ROIEndpoints') is not None:
            self.roiendpoints = m.get('ROIEndpoints')
        if m.get('RecistEndpoints') is not None:
            self.recist_endpoints = m.get('RecistEndpoints')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        return self


class ScreenChestCTResponseBodyDataScreenGCLesionOrganList(TeaModel):
    def __init__(
        self,
        diameter: List[float] = None,
        key_slice: int = None,
        roiendpoints: List[List[int]] = None,
        recist_endpoints: List[List[int]] = None,
        type: str = None,
    ):
        self.diameter = diameter
        self.key_slice = key_slice
        self.roiendpoints = roiendpoints
        self.recist_endpoints = recist_endpoints
        self.type = type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.diameter is not None:
            result['Diameter'] = self.diameter
        if self.key_slice is not None:
            result['KeySlice'] = self.key_slice
        if self.roiendpoints is not None:
            result['ROIEndpoints'] = self.roiendpoints
        if self.recist_endpoints is not None:
            result['RecistEndpoints'] = self.recist_endpoints
        if self.type is not None:
            result['Type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Diameter') is not None:
            self.diameter = m.get('Diameter')
        if m.get('KeySlice') is not None:
            self.key_slice = m.get('KeySlice')
        if m.get('ROIEndpoints') is not None:
            self.roiendpoints = m.get('ROIEndpoints')
        if m.get('RecistEndpoints') is not None:
            self.recist_endpoints = m.get('RecistEndpoints')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        return self


class ScreenChestCTResponseBodyDataScreenGCLesion(TeaModel):
    def __init__(
        self,
        gcvolume: str = None,
        lesion_list: List[ScreenChestCTResponseBodyDataScreenGCLesionLesionList] = None,
        mask: str = None,
        non_gcvolume: str = None,
        organ_list: List[ScreenChestCTResponseBodyDataScreenGCLesionOrganList] = None,
        probabilities: List[str] = None,
        stomach_volume: str = None,
    ):
        self.gcvolume = gcvolume
        self.lesion_list = lesion_list
        self.mask = mask
        self.non_gcvolume = non_gcvolume
        self.organ_list = organ_list
        self.probabilities = probabilities
        self.stomach_volume = stomach_volume

    def validate(self):
        if self.lesion_list:
            for k in self.lesion_list:
                if k:
                    k.validate()
        if self.organ_list:
            for k in self.organ_list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.gcvolume is not None:
            result['GCVolume'] = self.gcvolume
        result['LesionList'] = []
        if self.lesion_list is not None:
            for k in self.lesion_list:
                result['LesionList'].append(k.to_map() if k else None)
        if self.mask is not None:
            result['Mask'] = self.mask
        if self.non_gcvolume is not None:
            result['NonGCVolume'] = self.non_gcvolume
        result['OrganList'] = []
        if self.organ_list is not None:
            for k in self.organ_list:
                result['OrganList'].append(k.to_map() if k else None)
        if self.probabilities is not None:
            result['Probabilities'] = self.probabilities
        if self.stomach_volume is not None:
            result['StomachVolume'] = self.stomach_volume
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GCVolume') is not None:
            self.gcvolume = m.get('GCVolume')
        self.lesion_list = []
        if m.get('LesionList') is not None:
            for k in m.get('LesionList'):
                temp_model = ScreenChestCTResponseBodyDataScreenGCLesionLesionList()
                self.lesion_list.append(temp_model.from_map(k))
        if m.get('Mask') is not None:
            self.mask = m.get('Mask')
        if m.get('NonGCVolume') is not None:
            self.non_gcvolume = m.get('NonGCVolume')
        self.organ_list = []
        if m.get('OrganList') is not None:
            for k in m.get('OrganList'):
                temp_model = ScreenChestCTResponseBodyDataScreenGCLesionOrganList()
                self.organ_list.append(temp_model.from_map(k))
        if m.get('Probabilities') is not None:
            self.probabilities = m.get('Probabilities')
        if m.get('StomachVolume') is not None:
            self.stomach_volume = m.get('StomachVolume')
        return self


class ScreenChestCTResponseBodyDataScreenGC(TeaModel):
    def __init__(
        self,
        lesion: ScreenChestCTResponseBodyDataScreenGCLesion = None,
        series_instance_uid: str = None,
    ):
        self.lesion = lesion
        self.series_instance_uid = series_instance_uid

    def validate(self):
        if self.lesion:
            self.lesion.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lesion is not None:
            result['Lesion'] = self.lesion.to_map()
        if self.series_instance_uid is not None:
            result['SeriesInstanceUid'] = self.series_instance_uid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lesion') is not None:
            temp_model = ScreenChestCTResponseBodyDataScreenGCLesion()
            self.lesion = temp_model.from_map(m['Lesion'])
        if m.get('SeriesInstanceUid') is not None:
            self.series_instance_uid = m.get('SeriesInstanceUid')
        return self


class ScreenChestCTResponseBodyDataScreenLCLesionLesionListScoreAllClasses(TeaModel):
    def __init__(
        self,
        benign_prob: float = None,
        calc_prob: float = None,
        cyst_prob: float = None,
        malignant_prob: float = None,
    ):
        self.benign_prob = benign_prob
        self.calc_prob = calc_prob
        self.cyst_prob = cyst_prob
        self.malignant_prob = malignant_prob

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.benign_prob is not None:
            result['BenignProb'] = self.benign_prob
        if self.calc_prob is not None:
            result['CalcProb'] = self.calc_prob
        if self.cyst_prob is not None:
            result['CystProb'] = self.cyst_prob
        if self.malignant_prob is not None:
            result['MalignantProb'] = self.malignant_prob
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BenignProb') is not None:
            self.benign_prob = m.get('BenignProb')
        if m.get('CalcProb') is not None:
            self.calc_prob = m.get('CalcProb')
        if m.get('CystProb') is not None:
            self.cyst_prob = m.get('CystProb')
        if m.get('MalignantProb') is not None:
            self.malignant_prob = m.get('MalignantProb')
        return self


class ScreenChestCTResponseBodyDataScreenLCLesionLesionList(TeaModel):
    def __init__(
        self,
        diameter: List[float] = None,
        key_slice: int = None,
        malignancy: float = None,
        recist_endpoints: List[float] = None,
        score_all_classes: ScreenChestCTResponseBodyDataScreenLCLesionLesionListScoreAllClasses = None,
        type: str = None,
        volume: float = None,
    ):
        self.diameter = diameter
        self.key_slice = key_slice
        self.malignancy = malignancy
        self.recist_endpoints = recist_endpoints
        self.score_all_classes = score_all_classes
        self.type = type
        self.volume = volume

    def validate(self):
        if self.score_all_classes:
            self.score_all_classes.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.diameter is not None:
            result['Diameter'] = self.diameter
        if self.key_slice is not None:
            result['KeySlice'] = self.key_slice
        if self.malignancy is not None:
            result['Malignancy'] = self.malignancy
        if self.recist_endpoints is not None:
            result['RecistEndpoints'] = self.recist_endpoints
        if self.score_all_classes is not None:
            result['ScoreAllClasses'] = self.score_all_classes.to_map()
        if self.type is not None:
            result['Type'] = self.type
        if self.volume is not None:
            result['Volume'] = self.volume
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Diameter') is not None:
            self.diameter = m.get('Diameter')
        if m.get('KeySlice') is not None:
            self.key_slice = m.get('KeySlice')
        if m.get('Malignancy') is not None:
            self.malignancy = m.get('Malignancy')
        if m.get('RecistEndpoints') is not None:
            self.recist_endpoints = m.get('RecistEndpoints')
        if m.get('ScoreAllClasses') is not None:
            temp_model = ScreenChestCTResponseBodyDataScreenLCLesionLesionListScoreAllClasses()
            self.score_all_classes = temp_model.from_map(m['ScoreAllClasses'])
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Volume') is not None:
            self.volume = m.get('Volume')
        return self


class ScreenChestCTResponseBodyDataScreenLCLesionPatientLevelResult(TeaModel):
    def __init__(
        self,
        benign_non_cyst_prob: str = None,
        benign_prob: str = None,
        calc_prob: str = None,
        cyst_prob: str = None,
        hccprob: str = None,
        malignant_non_hccprob: str = None,
        malignant_prob: str = None,
    ):
        self.benign_non_cyst_prob = benign_non_cyst_prob
        self.benign_prob = benign_prob
        self.calc_prob = calc_prob
        self.cyst_prob = cyst_prob
        self.hccprob = hccprob
        self.malignant_non_hccprob = malignant_non_hccprob
        self.malignant_prob = malignant_prob

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.benign_non_cyst_prob is not None:
            result['BenignNonCystProb'] = self.benign_non_cyst_prob
        if self.benign_prob is not None:
            result['BenignProb'] = self.benign_prob
        if self.calc_prob is not None:
            result['CalcProb'] = self.calc_prob
        if self.cyst_prob is not None:
            result['CystProb'] = self.cyst_prob
        if self.hccprob is not None:
            result['HCCProb'] = self.hccprob
        if self.malignant_non_hccprob is not None:
            result['MalignantNonHCCProb'] = self.malignant_non_hccprob
        if self.malignant_prob is not None:
            result['MalignantProb'] = self.malignant_prob
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BenignNonCystProb') is not None:
            self.benign_non_cyst_prob = m.get('BenignNonCystProb')
        if m.get('BenignProb') is not None:
            self.benign_prob = m.get('BenignProb')
        if m.get('CalcProb') is not None:
            self.calc_prob = m.get('CalcProb')
        if m.get('CystProb') is not None:
            self.cyst_prob = m.get('CystProb')
        if m.get('HCCProb') is not None:
            self.hccprob = m.get('HCCProb')
        if m.get('MalignantNonHCCProb') is not None:
            self.malignant_non_hccprob = m.get('MalignantNonHCCProb')
        if m.get('MalignantProb') is not None:
            self.malignant_prob = m.get('MalignantProb')
        return self


class ScreenChestCTResponseBodyDataScreenLCLesion(TeaModel):
    def __init__(
        self,
        lesion_list: List[ScreenChestCTResponseBodyDataScreenLCLesionLesionList] = None,
        liver_volume: str = None,
        mask: str = None,
        patient_level_prob: float = None,
        patient_level_result: ScreenChestCTResponseBodyDataScreenLCLesionPatientLevelResult = None,
    ):
        self.lesion_list = lesion_list
        self.liver_volume = liver_volume
        self.mask = mask
        self.patient_level_prob = patient_level_prob
        self.patient_level_result = patient_level_result

    def validate(self):
        if self.lesion_list:
            for k in self.lesion_list:
                if k:
                    k.validate()
        if self.patient_level_result:
            self.patient_level_result.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['LesionList'] = []
        if self.lesion_list is not None:
            for k in self.lesion_list:
                result['LesionList'].append(k.to_map() if k else None)
        if self.liver_volume is not None:
            result['LiverVolume'] = self.liver_volume
        if self.mask is not None:
            result['Mask'] = self.mask
        if self.patient_level_prob is not None:
            result['PatientLevelProb'] = self.patient_level_prob
        if self.patient_level_result is not None:
            result['PatientLevelResult'] = self.patient_level_result.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.lesion_list = []
        if m.get('LesionList') is not None:
            for k in m.get('LesionList'):
                temp_model = ScreenChestCTResponseBodyDataScreenLCLesionLesionList()
                self.lesion_list.append(temp_model.from_map(k))
        if m.get('LiverVolume') is not None:
            self.liver_volume = m.get('LiverVolume')
        if m.get('Mask') is not None:
            self.mask = m.get('Mask')
        if m.get('PatientLevelProb') is not None:
            self.patient_level_prob = m.get('PatientLevelProb')
        if m.get('PatientLevelResult') is not None:
            temp_model = ScreenChestCTResponseBodyDataScreenLCLesionPatientLevelResult()
            self.patient_level_result = temp_model.from_map(m['PatientLevelResult'])
        return self


class ScreenChestCTResponseBodyDataScreenLC(TeaModel):
    def __init__(
        self,
        lesion: ScreenChestCTResponseBodyDataScreenLCLesion = None,
        series_instance_uid: str = None,
    ):
        self.lesion = lesion
        self.series_instance_uid = series_instance_uid

    def validate(self):
        if self.lesion:
            self.lesion.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lesion is not None:
            result['Lesion'] = self.lesion.to_map()
        if self.series_instance_uid is not None:
            result['SeriesInstanceUid'] = self.series_instance_uid
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lesion') is not None:
            temp_model = ScreenChestCTResponseBodyDataScreenLCLesion()
            self.lesion = temp_model.from_map(m['Lesion'])
        if m.get('SeriesInstanceUid') is not None:
            self.series_instance_uid = m.get('SeriesInstanceUid')
        return self


class ScreenChestCTResponseBodyData(TeaModel):
    def __init__(
        self,
        analyze_chest_vessel: ScreenChestCTResponseBodyDataAnalyzeChestVessel = None,
        cacs: ScreenChestCTResponseBodyDataCACS = None,
        calc_bmd: ScreenChestCTResponseBodyDataCalcBMD = None,
        covid: ScreenChestCTResponseBodyDataCovid = None,
        detect_ad: ScreenChestCTResponseBodyDataDetectAD = None,
        detect_liver_steatosis: ScreenChestCTResponseBodyDataDetectLiverSteatosis = None,
        detect_lymph: ScreenChestCTResponseBodyDataDetectLymph = None,
        detect_pdac: ScreenChestCTResponseBodyDataDetectPdac = None,
        detect_rib_fracture: ScreenChestCTResponseBodyDataDetectRibFracture = None,
        error_message: str = None,
        lung_nodule: ScreenChestCTResponseBodyDataLungNodule = None,
        muscle_fat: ScreenChestCTResponseBodyDataMuscleFat = None,
        nested_url_list: Dict[str, Any] = None,
        predict_cvd: ScreenChestCTResponseBodyDataPredictCVD = None,
        screen_bc: ScreenChestCTResponseBodyDataScreenBC = None,
        screen_crc: ScreenChestCTResponseBodyDataScreenCRC = None,
        screen_ec: ScreenChestCTResponseBodyDataScreenEc = None,
        screen_gc: ScreenChestCTResponseBodyDataScreenGC = None,
        screen_lc: ScreenChestCTResponseBodyDataScreenLC = None,
        urllist: Dict[str, Any] = None,
    ):
        self.analyze_chest_vessel = analyze_chest_vessel
        self.cacs = cacs
        self.calc_bmd = calc_bmd
        self.covid = covid
        self.detect_ad = detect_ad
        self.detect_liver_steatosis = detect_liver_steatosis
        self.detect_lymph = detect_lymph
        self.detect_pdac = detect_pdac
        self.detect_rib_fracture = detect_rib_fracture
        self.error_message = error_message
        self.lung_nodule = lung_nodule
        self.muscle_fat = muscle_fat
        self.nested_url_list = nested_url_list
        self.predict_cvd = predict_cvd
        self.screen_bc = screen_bc
        self.screen_crc = screen_crc
        self.screen_ec = screen_ec
        self.screen_gc = screen_gc
        self.screen_lc = screen_lc
        self.urllist = urllist

    def validate(self):
        if self.analyze_chest_vessel:
            self.analyze_chest_vessel.validate()
        if self.cacs:
            self.cacs.validate()
        if self.calc_bmd:
            self.calc_bmd.validate()
        if self.covid:
            self.covid.validate()
        if self.detect_ad:
            self.detect_ad.validate()
        if self.detect_liver_steatosis:
            self.detect_liver_steatosis.validate()
        if self.detect_lymph:
            self.detect_lymph.validate()
        if self.detect_pdac:
            self.detect_pdac.validate()
        if self.detect_rib_fracture:
            self.detect_rib_fracture.validate()
        if self.lung_nodule:
            self.lung_nodule.validate()
        if self.muscle_fat:
            self.muscle_fat.validate()
        if self.predict_cvd:
            self.predict_cvd.validate()
        if self.screen_bc:
            self.screen_bc.validate()
        if self.screen_crc:
            self.screen_crc.validate()
        if self.screen_ec:
            self.screen_ec.validate()
        if self.screen_gc:
            self.screen_gc.validate()
        if self.screen_lc:
            self.screen_lc.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.analyze_chest_vessel is not None:
            result['AnalyzeChestVessel'] = self.analyze_chest_vessel.to_map()
        if self.cacs is not None:
            result['CACS'] = self.cacs.to_map()
        if self.calc_bmd is not None:
            result['CalcBMD'] = self.calc_bmd.to_map()
        if self.covid is not None:
            result['Covid'] = self.covid.to_map()
        if self.detect_ad is not None:
            result['DetectAD'] = self.detect_ad.to_map()
        if self.detect_liver_steatosis is not None:
            result['DetectLiverSteatosis'] = self.detect_liver_steatosis.to_map()
        if self.detect_lymph is not None:
            result['DetectLymph'] = self.detect_lymph.to_map()
        if self.detect_pdac is not None:
            result['DetectPdac'] = self.detect_pdac.to_map()
        if self.detect_rib_fracture is not None:
            result['DetectRibFracture'] = self.detect_rib_fracture.to_map()
        if self.error_message is not None:
            result['ErrorMessage'] = self.error_message
        if self.lung_nodule is not None:
            result['LungNodule'] = self.lung_nodule.to_map()
        if self.muscle_fat is not None:
            result['MuscleFat'] = self.muscle_fat.to_map()
        if self.nested_url_list is not None:
            result['NestedUrlList'] = self.nested_url_list
        if self.predict_cvd is not None:
            result['PredictCVD'] = self.predict_cvd.to_map()
        if self.screen_bc is not None:
            result['ScreenBC'] = self.screen_bc.to_map()
        if self.screen_crc is not None:
            result['ScreenCRC'] = self.screen_crc.to_map()
        if self.screen_ec is not None:
            result['ScreenEc'] = self.screen_ec.to_map()
        if self.screen_gc is not None:
            result['ScreenGC'] = self.screen_gc.to_map()
        if self.screen_lc is not None:
            result['ScreenLC'] = self.screen_lc.to_map()
        if self.urllist is not None:
            result['URLList'] = self.urllist
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AnalyzeChestVessel') is not None:
            temp_model = ScreenChestCTResponseBodyDataAnalyzeChestVessel()
            self.analyze_chest_vessel = temp_model.from_map(m['AnalyzeChestVessel'])
        if m.get('CACS') is not None:
            temp_model = ScreenChestCTResponseBodyDataCACS()
            self.cacs = temp_model.from_map(m['CACS'])
        if m.get('CalcBMD') is not None:
            temp_model = ScreenChestCTResponseBodyDataCalcBMD()
            self.calc_bmd = temp_model.from_map(m['CalcBMD'])
        if m.get('Covid') is not None:
            temp_model = ScreenChestCTResponseBodyDataCovid()
            self.covid = temp_model.from_map(m['Covid'])
        if m.get('DetectAD') is not None:
            temp_model = ScreenChestCTResponseBodyDataDetectAD()
            self.detect_ad = temp_model.from_map(m['DetectAD'])
        if m.get('DetectLiverSteatosis') is not None:
            temp_model = ScreenChestCTResponseBodyDataDetectLiverSteatosis()
            self.detect_liver_steatosis = temp_model.from_map(m['DetectLiverSteatosis'])
        if m.get('DetectLymph') is not None:
            temp_model = ScreenChestCTResponseBodyDataDetectLymph()
            self.detect_lymph = temp_model.from_map(m['DetectLymph'])
        if m.get('DetectPdac') is not None:
            temp_model = ScreenChestCTResponseBodyDataDetectPdac()
            self.detect_pdac = temp_model.from_map(m['DetectPdac'])
        if m.get('DetectRibFracture') is not None:
            temp_model = ScreenChestCTResponseBodyDataDetectRibFracture()
            self.detect_rib_fracture = temp_model.from_map(m['DetectRibFracture'])
        if m.get('ErrorMessage') is not None:
            self.error_message = m.get('ErrorMessage')
        if m.get('LungNodule') is not None:
            temp_model = ScreenChestCTResponseBodyDataLungNodule()
            self.lung_nodule = temp_model.from_map(m['LungNodule'])
        if m.get('MuscleFat') is not None:
            temp_model = ScreenChestCTResponseBodyDataMuscleFat()
            self.muscle_fat = temp_model.from_map(m['MuscleFat'])
        if m.get('NestedUrlList') is not None:
            self.nested_url_list = m.get('NestedUrlList')
        if m.get('PredictCVD') is not None:
            temp_model = ScreenChestCTResponseBodyDataPredictCVD()
            self.predict_cvd = temp_model.from_map(m['PredictCVD'])
        if m.get('ScreenBC') is not None:
            temp_model = ScreenChestCTResponseBodyDataScreenBC()
            self.screen_bc = temp_model.from_map(m['ScreenBC'])
        if m.get('ScreenCRC') is not None:
            temp_model = ScreenChestCTResponseBodyDataScreenCRC()
            self.screen_crc = temp_model.from_map(m['ScreenCRC'])
        if m.get('ScreenEc') is not None:
            temp_model = ScreenChestCTResponseBodyDataScreenEc()
            self.screen_ec = temp_model.from_map(m['ScreenEc'])
        if m.get('ScreenGC') is not None:
            temp_model = ScreenChestCTResponseBodyDataScreenGC()
            self.screen_gc = temp_model.from_map(m['ScreenGC'])
        if m.get('ScreenLC') is not None:
            temp_model = ScreenChestCTResponseBodyDataScreenLC()
            self.screen_lc = temp_model.from_map(m['ScreenLC'])
        if m.get('URLList') is not None:
            self.urllist = m.get('URLList')
        return self


class ScreenChestCTResponseBody(TeaModel):
    def __init__(
        self,
        data: ScreenChestCTResponseBodyData = None,
        message: str = None,
        request_id: str = None,
    ):
        self.data = data
        self.message = message
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = ScreenChestCTResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ScreenChestCTResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ScreenChestCTResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ScreenChestCTResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ScreenECRequestURLList(TeaModel):
    def __init__(
        self,
        url: str = None,
    ):
        # This parameter is required.
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.url is not None:
            result['URL'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.url = m.get('URL')
        return self


class ScreenECRequest(TeaModel):
    def __init__(
        self,
        data_source_type: str = None,
        urllist: List[ScreenECRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_source_type = data_source_type
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_source_type is not None:
            result['DataSourceType'] = self.data_source_type
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataSourceType') is not None:
            self.data_source_type = m.get('DataSourceType')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = ScreenECRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class ScreenECAdvanceRequestURLList(TeaModel):
    def __init__(
        self,
        urlobject: BinaryIO = None,
    ):
        # This parameter is required.
        self.urlobject = urlobject

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.urlobject is not None:
            result['URL'] = self.urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.urlobject = m.get('URL')
        return self


class ScreenECAdvanceRequest(TeaModel):
    def __init__(
        self,
        data_source_type: str = None,
        urllist: List[ScreenECAdvanceRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_source_type = data_source_type
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_source_type is not None:
            result['DataSourceType'] = self.data_source_type
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataSourceType') is not None:
            self.data_source_type = m.get('DataSourceType')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = ScreenECAdvanceRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class ScreenECResponseBodyDataLesion(TeaModel):
    def __init__(
        self,
        benign_volume: str = None,
        ec_volume: str = None,
        eso_volume: str = None,
        mask: str = None,
        possibilities: List[str] = None,
    ):
        self.benign_volume = benign_volume
        self.ec_volume = ec_volume
        self.eso_volume = eso_volume
        self.mask = mask
        self.possibilities = possibilities

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.benign_volume is not None:
            result['BenignVolume'] = self.benign_volume
        if self.ec_volume is not None:
            result['EcVolume'] = self.ec_volume
        if self.eso_volume is not None:
            result['EsoVolume'] = self.eso_volume
        if self.mask is not None:
            result['Mask'] = self.mask
        if self.possibilities is not None:
            result['Possibilities'] = self.possibilities
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BenignVolume') is not None:
            self.benign_volume = m.get('BenignVolume')
        if m.get('EcVolume') is not None:
            self.ec_volume = m.get('EcVolume')
        if m.get('EsoVolume') is not None:
            self.eso_volume = m.get('EsoVolume')
        if m.get('Mask') is not None:
            self.mask = m.get('Mask')
        if m.get('Possibilities') is not None:
            self.possibilities = m.get('Possibilities')
        return self


class ScreenECResponseBodyData(TeaModel):
    def __init__(
        self,
        lesion: ScreenECResponseBodyDataLesion = None,
    ):
        self.lesion = lesion

    def validate(self):
        if self.lesion:
            self.lesion.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lesion is not None:
            result['Lesion'] = self.lesion.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lesion') is not None:
            temp_model = ScreenECResponseBodyDataLesion()
            self.lesion = temp_model.from_map(m['Lesion'])
        return self


class ScreenECResponseBody(TeaModel):
    def __init__(
        self,
        data: ScreenECResponseBodyData = None,
        message: str = None,
        request_id: str = None,
    ):
        self.data = data
        self.message = message
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = ScreenECResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ScreenECResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ScreenECResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ScreenECResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ScreenGCRequestURLList(TeaModel):
    def __init__(
        self,
        url: str = None,
    ):
        # This parameter is required.
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.url is not None:
            result['URL'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.url = m.get('URL')
        return self


class ScreenGCRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        data_source_type: str = None,
        org_id: str = None,
        org_name: str = None,
        urllist: List[ScreenGCRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.data_source_type = data_source_type
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.data_source_type is not None:
            result['DataSourceType'] = self.data_source_type
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('DataSourceType') is not None:
            self.data_source_type = m.get('DataSourceType')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = ScreenGCRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class ScreenGCAdvanceRequestURLList(TeaModel):
    def __init__(
        self,
        urlobject: BinaryIO = None,
    ):
        # This parameter is required.
        self.urlobject = urlobject

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.urlobject is not None:
            result['URL'] = self.urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.urlobject = m.get('URL')
        return self


class ScreenGCAdvanceRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        data_source_type: str = None,
        org_id: str = None,
        org_name: str = None,
        urllist: List[ScreenGCAdvanceRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.data_source_type = data_source_type
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.data_source_type is not None:
            result['DataSourceType'] = self.data_source_type
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('DataSourceType') is not None:
            self.data_source_type = m.get('DataSourceType')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = ScreenGCAdvanceRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class ScreenGCResponseBodyDataLesion(TeaModel):
    def __init__(
        self,
        gcvolume: str = None,
        mask: str = None,
        non_gcvolume: str = None,
        probabilities: str = None,
        stomach_volume: str = None,
    ):
        self.gcvolume = gcvolume
        self.mask = mask
        self.non_gcvolume = non_gcvolume
        self.probabilities = probabilities
        self.stomach_volume = stomach_volume

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.gcvolume is not None:
            result['GCVolume'] = self.gcvolume
        if self.mask is not None:
            result['Mask'] = self.mask
        if self.non_gcvolume is not None:
            result['NonGCVolume'] = self.non_gcvolume
        if self.probabilities is not None:
            result['Probabilities'] = self.probabilities
        if self.stomach_volume is not None:
            result['StomachVolume'] = self.stomach_volume
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('GCVolume') is not None:
            self.gcvolume = m.get('GCVolume')
        if m.get('Mask') is not None:
            self.mask = m.get('Mask')
        if m.get('NonGCVolume') is not None:
            self.non_gcvolume = m.get('NonGCVolume')
        if m.get('Probabilities') is not None:
            self.probabilities = m.get('Probabilities')
        if m.get('StomachVolume') is not None:
            self.stomach_volume = m.get('StomachVolume')
        return self


class ScreenGCResponseBodyData(TeaModel):
    def __init__(
        self,
        lesion: ScreenGCResponseBodyDataLesion = None,
    ):
        self.lesion = lesion

    def validate(self):
        if self.lesion:
            self.lesion.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lesion is not None:
            result['Lesion'] = self.lesion.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lesion') is not None:
            temp_model = ScreenGCResponseBodyDataLesion()
            self.lesion = temp_model.from_map(m['Lesion'])
        return self


class ScreenGCResponseBody(TeaModel):
    def __init__(
        self,
        data: ScreenGCResponseBodyData = None,
        message: str = None,
        request_id: str = None,
    ):
        self.data = data
        self.message = message
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = ScreenGCResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ScreenGCResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ScreenGCResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ScreenGCResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ScreenLCRequestURLList(TeaModel):
    def __init__(
        self,
        url: str = None,
    ):
        # This parameter is required.
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.url is not None:
            result['URL'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.url = m.get('URL')
        return self


class ScreenLCRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        data_source_type: str = None,
        org_id: str = None,
        org_name: str = None,
        urllist: List[ScreenLCRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.data_source_type = data_source_type
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.data_source_type is not None:
            result['DataSourceType'] = self.data_source_type
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('DataSourceType') is not None:
            self.data_source_type = m.get('DataSourceType')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = ScreenLCRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class ScreenLCAdvanceRequestURLList(TeaModel):
    def __init__(
        self,
        urlobject: BinaryIO = None,
    ):
        # This parameter is required.
        self.urlobject = urlobject

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.urlobject is not None:
            result['URL'] = self.urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.urlobject = m.get('URL')
        return self


class ScreenLCAdvanceRequest(TeaModel):
    def __init__(
        self,
        data_format: str = None,
        data_source_type: str = None,
        org_id: str = None,
        org_name: str = None,
        urllist: List[ScreenLCAdvanceRequestURLList] = None,
    ):
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.data_source_type = data_source_type
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.data_source_type is not None:
            result['DataSourceType'] = self.data_source_type
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('DataSourceType') is not None:
            self.data_source_type = m.get('DataSourceType')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = ScreenLCAdvanceRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class ScreenLCResponseBodyDataLesionLesionListScoreAllClassesProb(TeaModel):
    def __init__(
        self,
        benign_prob: float = None,
        calc_prob: float = None,
        cyst_prob: float = None,
        malignant_prob: float = None,
    ):
        self.benign_prob = benign_prob
        self.calc_prob = calc_prob
        self.cyst_prob = cyst_prob
        self.malignant_prob = malignant_prob

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.benign_prob is not None:
            result['BenignProb'] = self.benign_prob
        if self.calc_prob is not None:
            result['CalcProb'] = self.calc_prob
        if self.cyst_prob is not None:
            result['CystProb'] = self.cyst_prob
        if self.malignant_prob is not None:
            result['MalignantProb'] = self.malignant_prob
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BenignProb') is not None:
            self.benign_prob = m.get('BenignProb')
        if m.get('CalcProb') is not None:
            self.calc_prob = m.get('CalcProb')
        if m.get('CystProb') is not None:
            self.cyst_prob = m.get('CystProb')
        if m.get('MalignantProb') is not None:
            self.malignant_prob = m.get('MalignantProb')
        return self


class ScreenLCResponseBodyDataLesionLesionList(TeaModel):
    def __init__(
        self,
        diameter: List[float] = None,
        key_slice: int = None,
        malignancy: float = None,
        recist_endpoints: List[float] = None,
        score_all_classes_prob: ScreenLCResponseBodyDataLesionLesionListScoreAllClassesProb = None,
        type: str = None,
        volume: float = None,
    ):
        self.diameter = diameter
        self.key_slice = key_slice
        self.malignancy = malignancy
        self.recist_endpoints = recist_endpoints
        self.score_all_classes_prob = score_all_classes_prob
        self.type = type
        self.volume = volume

    def validate(self):
        if self.score_all_classes_prob:
            self.score_all_classes_prob.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.diameter is not None:
            result['Diameter'] = self.diameter
        if self.key_slice is not None:
            result['KeySlice'] = self.key_slice
        if self.malignancy is not None:
            result['Malignancy'] = self.malignancy
        if self.recist_endpoints is not None:
            result['RecistEndpoints'] = self.recist_endpoints
        if self.score_all_classes_prob is not None:
            result['ScoreAllClassesProb'] = self.score_all_classes_prob.to_map()
        if self.type is not None:
            result['Type'] = self.type
        if self.volume is not None:
            result['Volume'] = self.volume
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Diameter') is not None:
            self.diameter = m.get('Diameter')
        if m.get('KeySlice') is not None:
            self.key_slice = m.get('KeySlice')
        if m.get('Malignancy') is not None:
            self.malignancy = m.get('Malignancy')
        if m.get('RecistEndpoints') is not None:
            self.recist_endpoints = m.get('RecistEndpoints')
        if m.get('ScoreAllClassesProb') is not None:
            temp_model = ScreenLCResponseBodyDataLesionLesionListScoreAllClassesProb()
            self.score_all_classes_prob = temp_model.from_map(m['ScoreAllClassesProb'])
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Volume') is not None:
            self.volume = m.get('Volume')
        return self


class ScreenLCResponseBodyDataLesionPatientLevelResult(TeaModel):
    def __init__(
        self,
        benign_non_cyst_prob: str = None,
        benign_prob: float = None,
        calc_prob: float = None,
        cyst_prob: float = None,
        hccprob: float = None,
        malignant_non_hccprob: float = None,
        malignant_prob: float = None,
    ):
        self.benign_non_cyst_prob = benign_non_cyst_prob
        self.benign_prob = benign_prob
        self.calc_prob = calc_prob
        self.cyst_prob = cyst_prob
        self.hccprob = hccprob
        self.malignant_non_hccprob = malignant_non_hccprob
        self.malignant_prob = malignant_prob

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.benign_non_cyst_prob is not None:
            result['BenignNonCystProb'] = self.benign_non_cyst_prob
        if self.benign_prob is not None:
            result['BenignProb'] = self.benign_prob
        if self.calc_prob is not None:
            result['CalcProb'] = self.calc_prob
        if self.cyst_prob is not None:
            result['CystProb'] = self.cyst_prob
        if self.hccprob is not None:
            result['HCCProb'] = self.hccprob
        if self.malignant_non_hccprob is not None:
            result['MalignantNonHCCProb'] = self.malignant_non_hccprob
        if self.malignant_prob is not None:
            result['MalignantProb'] = self.malignant_prob
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BenignNonCystProb') is not None:
            self.benign_non_cyst_prob = m.get('BenignNonCystProb')
        if m.get('BenignProb') is not None:
            self.benign_prob = m.get('BenignProb')
        if m.get('CalcProb') is not None:
            self.calc_prob = m.get('CalcProb')
        if m.get('CystProb') is not None:
            self.cyst_prob = m.get('CystProb')
        if m.get('HCCProb') is not None:
            self.hccprob = m.get('HCCProb')
        if m.get('MalignantNonHCCProb') is not None:
            self.malignant_non_hccprob = m.get('MalignantNonHCCProb')
        if m.get('MalignantProb') is not None:
            self.malignant_prob = m.get('MalignantProb')
        return self


class ScreenLCResponseBodyDataLesion(TeaModel):
    def __init__(
        self,
        lesion_list: List[ScreenLCResponseBodyDataLesionLesionList] = None,
        liver_volume: float = None,
        mask: str = None,
        patient_level_prob: float = None,
        patient_level_result: ScreenLCResponseBodyDataLesionPatientLevelResult = None,
    ):
        self.lesion_list = lesion_list
        self.liver_volume = liver_volume
        self.mask = mask
        self.patient_level_prob = patient_level_prob
        self.patient_level_result = patient_level_result

    def validate(self):
        if self.lesion_list:
            for k in self.lesion_list:
                if k:
                    k.validate()
        if self.patient_level_result:
            self.patient_level_result.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['LesionList'] = []
        if self.lesion_list is not None:
            for k in self.lesion_list:
                result['LesionList'].append(k.to_map() if k else None)
        if self.liver_volume is not None:
            result['LiverVolume'] = self.liver_volume
        if self.mask is not None:
            result['Mask'] = self.mask
        if self.patient_level_prob is not None:
            result['PatientLevelProb'] = self.patient_level_prob
        if self.patient_level_result is not None:
            result['PatientLevelResult'] = self.patient_level_result.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.lesion_list = []
        if m.get('LesionList') is not None:
            for k in m.get('LesionList'):
                temp_model = ScreenLCResponseBodyDataLesionLesionList()
                self.lesion_list.append(temp_model.from_map(k))
        if m.get('LiverVolume') is not None:
            self.liver_volume = m.get('LiverVolume')
        if m.get('Mask') is not None:
            self.mask = m.get('Mask')
        if m.get('PatientLevelProb') is not None:
            self.patient_level_prob = m.get('PatientLevelProb')
        if m.get('PatientLevelResult') is not None:
            temp_model = ScreenLCResponseBodyDataLesionPatientLevelResult()
            self.patient_level_result = temp_model.from_map(m['PatientLevelResult'])
        return self


class ScreenLCResponseBodyData(TeaModel):
    def __init__(
        self,
        lesion: ScreenLCResponseBodyDataLesion = None,
    ):
        self.lesion = lesion

    def validate(self):
        if self.lesion:
            self.lesion.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.lesion is not None:
            result['Lesion'] = self.lesion.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Lesion') is not None:
            temp_model = ScreenLCResponseBodyDataLesion()
            self.lesion = temp_model.from_map(m['Lesion'])
        return self


class ScreenLCResponseBody(TeaModel):
    def __init__(
        self,
        data: ScreenLCResponseBodyData = None,
        message: str = None,
        request_id: str = None,
    ):
        self.data = data
        self.message = message
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = ScreenLCResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ScreenLCResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: ScreenLCResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = ScreenLCResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SegmentLymphNodeRequestURLList(TeaModel):
    def __init__(
        self,
        url: str = None,
    ):
        # This parameter is required.
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.url is not None:
            result['URL'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.url = m.get('URL')
        return self


class SegmentLymphNodeRequest(TeaModel):
    def __init__(
        self,
        body_part: str = None,
        data_format: str = None,
        org_id: str = None,
        org_name: str = None,
        urllist: List[SegmentLymphNodeRequestURLList] = None,
    ):
        # This parameter is required.
        self.body_part = body_part
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.body_part is not None:
            result['BodyPart'] = self.body_part
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BodyPart') is not None:
            self.body_part = m.get('BodyPart')
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = SegmentLymphNodeRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class SegmentLymphNodeAdvanceRequestURLList(TeaModel):
    def __init__(
        self,
        urlobject: BinaryIO = None,
    ):
        # This parameter is required.
        self.urlobject = urlobject

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.urlobject is not None:
            result['URL'] = self.urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.urlobject = m.get('URL')
        return self


class SegmentLymphNodeAdvanceRequest(TeaModel):
    def __init__(
        self,
        body_part: str = None,
        data_format: str = None,
        org_id: str = None,
        org_name: str = None,
        urllist: List[SegmentLymphNodeAdvanceRequestURLList] = None,
    ):
        # This parameter is required.
        self.body_part = body_part
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.body_part is not None:
            result['BodyPart'] = self.body_part
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BodyPart') is not None:
            self.body_part = m.get('BodyPart')
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = SegmentLymphNodeAdvanceRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class SegmentLymphNodeResponseBodyData(TeaModel):
    def __init__(
        self,
        result_url: str = None,
    ):
        self.result_url = result_url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.result_url is not None:
            result['ResultURL'] = self.result_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ResultURL') is not None:
            self.result_url = m.get('ResultURL')
        return self


class SegmentLymphNodeResponseBody(TeaModel):
    def __init__(
        self,
        data: SegmentLymphNodeResponseBodyData = None,
        message: str = None,
        request_id: str = None,
    ):
        self.data = data
        self.message = message
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = SegmentLymphNodeResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class SegmentLymphNodeResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: SegmentLymphNodeResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = SegmentLymphNodeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SegmentOARRequestURLList(TeaModel):
    def __init__(
        self,
        url: str = None,
    ):
        # This parameter is required.
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.url is not None:
            result['URL'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.url = m.get('URL')
        return self


class SegmentOARRequest(TeaModel):
    def __init__(
        self,
        body_part: str = None,
        contrast: bool = None,
        data_format: str = None,
        mask_list: List[int] = None,
        org_id: str = None,
        org_name: str = None,
        urllist: List[SegmentOARRequestURLList] = None,
    ):
        self.body_part = body_part
        self.contrast = contrast
        # This parameter is required.
        self.data_format = data_format
        self.mask_list = mask_list
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.body_part is not None:
            result['BodyPart'] = self.body_part
        if self.contrast is not None:
            result['Contrast'] = self.contrast
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.mask_list is not None:
            result['MaskList'] = self.mask_list
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BodyPart') is not None:
            self.body_part = m.get('BodyPart')
        if m.get('Contrast') is not None:
            self.contrast = m.get('Contrast')
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('MaskList') is not None:
            self.mask_list = m.get('MaskList')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = SegmentOARRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class SegmentOARAdvanceRequestURLList(TeaModel):
    def __init__(
        self,
        urlobject: BinaryIO = None,
    ):
        # This parameter is required.
        self.urlobject = urlobject

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.urlobject is not None:
            result['URL'] = self.urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.urlobject = m.get('URL')
        return self


class SegmentOARAdvanceRequest(TeaModel):
    def __init__(
        self,
        body_part: str = None,
        contrast: bool = None,
        data_format: str = None,
        mask_list: List[int] = None,
        org_id: str = None,
        org_name: str = None,
        urllist: List[SegmentOARAdvanceRequestURLList] = None,
    ):
        self.body_part = body_part
        self.contrast = contrast
        # This parameter is required.
        self.data_format = data_format
        self.mask_list = mask_list
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.body_part is not None:
            result['BodyPart'] = self.body_part
        if self.contrast is not None:
            result['Contrast'] = self.contrast
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.mask_list is not None:
            result['MaskList'] = self.mask_list
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BodyPart') is not None:
            self.body_part = m.get('BodyPart')
        if m.get('Contrast') is not None:
            self.contrast = m.get('Contrast')
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('MaskList') is not None:
            self.mask_list = m.get('MaskList')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = SegmentOARAdvanceRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class SegmentOARResponseBodyData(TeaModel):
    def __init__(
        self,
        mask_list: List[str] = None,
        result_url: str = None,
    ):
        self.mask_list = mask_list
        self.result_url = result_url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.mask_list is not None:
            result['MaskList'] = self.mask_list
        if self.result_url is not None:
            result['ResultURL'] = self.result_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MaskList') is not None:
            self.mask_list = m.get('MaskList')
        if m.get('ResultURL') is not None:
            self.result_url = m.get('ResultURL')
        return self


class SegmentOARResponseBody(TeaModel):
    def __init__(
        self,
        data: SegmentOARResponseBodyData = None,
        message: str = None,
        request_id: str = None,
    ):
        self.data = data
        self.message = message
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = SegmentOARResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class SegmentOARResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: SegmentOARResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = SegmentOARResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class TargetVolumeSegmentRequestURLList(TeaModel):
    def __init__(
        self,
        url: str = None,
    ):
        # This parameter is required.
        self.url = url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.url is not None:
            result['URL'] = self.url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.url = m.get('URL')
        return self


class TargetVolumeSegmentRequest(TeaModel):
    def __init__(
        self,
        cancer_type: str = None,
        data_format: str = None,
        org_id: str = None,
        org_name: str = None,
        target_volume_type: str = None,
        urllist: List[TargetVolumeSegmentRequestURLList] = None,
    ):
        # This parameter is required.
        self.cancer_type = cancer_type
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.target_volume_type = target_volume_type
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cancer_type is not None:
            result['CancerType'] = self.cancer_type
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        if self.target_volume_type is not None:
            result['TargetVolumeType'] = self.target_volume_type
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CancerType') is not None:
            self.cancer_type = m.get('CancerType')
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        if m.get('TargetVolumeType') is not None:
            self.target_volume_type = m.get('TargetVolumeType')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = TargetVolumeSegmentRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class TargetVolumeSegmentAdvanceRequestURLList(TeaModel):
    def __init__(
        self,
        urlobject: BinaryIO = None,
    ):
        # This parameter is required.
        self.urlobject = urlobject

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.urlobject is not None:
            result['URL'] = self.urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('URL') is not None:
            self.urlobject = m.get('URL')
        return self


class TargetVolumeSegmentAdvanceRequest(TeaModel):
    def __init__(
        self,
        cancer_type: str = None,
        data_format: str = None,
        org_id: str = None,
        org_name: str = None,
        target_volume_type: str = None,
        urllist: List[TargetVolumeSegmentAdvanceRequestURLList] = None,
    ):
        # This parameter is required.
        self.cancer_type = cancer_type
        # This parameter is required.
        self.data_format = data_format
        # This parameter is required.
        self.org_id = org_id
        # This parameter is required.
        self.org_name = org_name
        # This parameter is required.
        self.target_volume_type = target_volume_type
        # This parameter is required.
        self.urllist = urllist

    def validate(self):
        if self.urllist:
            for k in self.urllist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.cancer_type is not None:
            result['CancerType'] = self.cancer_type
        if self.data_format is not None:
            result['DataFormat'] = self.data_format
        if self.org_id is not None:
            result['OrgId'] = self.org_id
        if self.org_name is not None:
            result['OrgName'] = self.org_name
        if self.target_volume_type is not None:
            result['TargetVolumeType'] = self.target_volume_type
        result['URLList'] = []
        if self.urllist is not None:
            for k in self.urllist:
                result['URLList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CancerType') is not None:
            self.cancer_type = m.get('CancerType')
        if m.get('DataFormat') is not None:
            self.data_format = m.get('DataFormat')
        if m.get('OrgId') is not None:
            self.org_id = m.get('OrgId')
        if m.get('OrgName') is not None:
            self.org_name = m.get('OrgName')
        if m.get('TargetVolumeType') is not None:
            self.target_volume_type = m.get('TargetVolumeType')
        self.urllist = []
        if m.get('URLList') is not None:
            for k in m.get('URLList'):
                temp_model = TargetVolumeSegmentAdvanceRequestURLList()
                self.urllist.append(temp_model.from_map(k))
        return self


class TargetVolumeSegmentResponseBodyData(TeaModel):
    def __init__(
        self,
        result_url: str = None,
    ):
        self.result_url = result_url

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.result_url is not None:
            result['ResultURL'] = self.result_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ResultURL') is not None:
            self.result_url = m.get('ResultURL')
        return self


class TargetVolumeSegmentResponseBody(TeaModel):
    def __init__(
        self,
        data: TargetVolumeSegmentResponseBodyData = None,
        message: str = None,
        request_id: str = None,
    ):
        self.data = data
        self.message = message
        self.request_id = request_id

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.message is not None:
            result['Message'] = self.message
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = TargetVolumeSegmentResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Message') is not None:
            self.message = m.get('Message')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class TargetVolumeSegmentResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        status_code: int = None,
        body: TargetVolumeSegmentResponseBody = None,
    ):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def validate(self):
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_code is not None:
            result['statusCode'] = self.status_code
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('statusCode') is not None:
            self.status_code = m.get('statusCode')
        if m.get('body') is not None:
            temp_model = TargetVolumeSegmentResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


