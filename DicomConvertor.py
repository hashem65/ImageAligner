'''
Created on 9/04/2016

@author: jagir
'''

import dicom, numpy as np
from PIL import Image
from dicom.dataset import Dataset, FileDataset, Tag


class Convertor(object):
    '''
    classdocs
    A jpg to dicom convertor based on pydicom and PIL
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
        
    def convert(self,imagefile,dicomfile,ox=0,oy=0,oz=0,xv=[1,0,0],yv=[0,1,0]):
        file_meta = Dataset()
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.7'  # 
        file_meta.MediaStorageSOPInstanceUID = dicom.UID.generate_uid()
        file_meta.ImplementationClassUID = file_meta.MediaStorageSOPInstanceUID
        
        # Create the FileDataset instance (initially no data elements, but file_meta supplied)
        
        ds = FileDataset(dicomfile, {}, file_meta=file_meta, preamble=b"\0" * 128)
        
        img = Image.open(imagefile)
        # Add the data elements -- not trying to set all required here. Check DICOM standard
        ds.PatientName = str(imagefile)
        val = np.random.randint(1,99999)
        ds.PatientID = '%05d' % (val)
        ds.SOPInstanceUID = dicom.UID.generate_uid()
        ds.add_new(Tag(0x20, 0x32), 'DS', [ox,oy,oz])
        ds.add_new(Tag(0x20, 0x37),'DS', xv+yv)
        ds.Columns = img.size[0] #img width
        ds.Rows = img.size[1] #img height

        #This is specific to the type of jpeg encoding
        #These parameters were obtained from the dicom created by using img2dcm tool of dcmtk
        #They seem to work for PIL loaded files
	if img.mode == 'L':
 	   ds.SamplesPerPixel=1
           ds.PhotometricInterpretation= 'MONOCHROME2' # Should match img.mode
        elif img.mode == 'RGB':
 	   ds.SamplesPerPixel=3
           ds.PhotometricInterpretation= 'RGB' # Should match img.mode
        ds.PixelSpacing = [1,1,1]
        ds.BitsAllocated= 8
        ds.BitsStored=8
        ds.HighBit=7
        ds.PixelRepresentation=0
        ds.LossyImageCompression='01'
        ds.LossyImageCompressionMethod= 'ISO_10918_1'
        #ds.TransferSyntaxIndex = '1.2.840.10008.1.2'
        ds.PixelData = np.array(img).tostring()
        ds.save_as(dicomfile)
        
        
        
if __name__ == '__main__':
    obj = Convertor()
    obj.convert('images.jpg', 'imageX.dcm',0,0,0,[1,0,0],[0,1,0])
    obj.convert('images.jpg', 'imageX.dcm',0,0,0,[1,0,0],[0,1,0])
    obj.convert('images.jpg', 'imageX.dcm',0,0,0,[1,0,0],[0,1,0])
