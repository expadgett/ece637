img=imread('house.tif');
[M,N]=size(img);
graymap=[0:255; 0:255; 0:255]'/255;
colormap(graymap);
img_thresh=zeros(size(img));
for i=1:M
    for j=1:N
        if img(i,j)>127
            img_thresh(i,j)=255;
        end
    end
end
image(img_thresh);
img_d=double(img);
img_thres_d=double(img_thresh);
RMSE=sqrt((1/(N*M))*sum(sum((img_d-img_thres_d).^2)))
fid=fidelity(img, img_thresh)

