data=Sub015_6MW_PPAFO_0005.Trajectories.Labeled.Data;
downsample = 2;
for i = 1:downsample:size(data,3)
    x=data(:,1,i);
    y=data(:,2,i);
    z=data(:,3,i);
    %xlabel('X-axis')
    %ylabel('Y-axis')
    %zyaleb('Z-axis')
    plot3(x,y,z,'b.')
    xlim([-2200,2000]);
    ylim([-500 100]);
    zlim([0 1500]);
    pause(1/(200/downsample));
    drawnow;
end

    


