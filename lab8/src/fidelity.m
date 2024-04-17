function fid=fidelity(f,b)
    f=double(f);
    b=double(b);

    f_1=255*(f/255).^2.2;
    sigma=2
    [i, j]=meshgrid(-3:1:3, -3:1:3);
    h=exp(-i.^2+j.^2)/(2*sigma);
    h=h/sum(h(:));
    f1h=conv2(f_1, h, 'same');
    b1h=conv2(b, h, 'same');
    flt=255*(f1h/255).^(1/3);
    blt=255*(b1h/255).^(1/3);
    [M, N]=size(flt);
    fid=sqrt((1/(N*M))*sum(sum((flt-blt).^2)));
end