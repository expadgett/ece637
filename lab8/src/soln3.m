img=imread('house.tif');
f1=255*(double(img)/255).^2.2;
[M,N]=size(img);

I2=[1,2;3,0];
I4=[4*I2+1, 4*I2+2,; 4*I2+3, 4*I2];
I8=[4*I4+1, 4*I4+2,; 4*I4+3, 4*I4];

T2=255*((I2+0.5)/(4));
T4=255*((I4+0.5)/(16));
T8=255*((I2+0.5)/(64));

f12=zeros(M,N);
f14=zeros(M,N);
f18=zeros(M,N);

for p=1:M
    for q=1:N
        i=mod(p-1, 2)+1;
        j=mod(q-1, 2)+1;
        if f1(p,q)>T2(i,j)
            f12(p,q)=255;
        else
            f12(p,q)=0;
        end
    end
end
imwrite(f12, 'houseN2.tif')
img_d=double(img);
RMSE=sqrt((1/(N*M))*sum(sum(((img_d-f12).^2))))