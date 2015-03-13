clf

data=Sub003_6MW_AFO_0001.Trajectories.Labeled.Data;

x=data(:,1,:);
sacralset=x(1, :);
index=linspace(1, length(sacralset), length(sacralset));

plot(index, sacralset, '-')
xlabel('Time in Frames', 'fontsize', 20)
ylabel('X Position in Millimeters', 'fontsize', 20)
title('Time Series Plot for Participant 1 Wearing AFO in Trial 5', 'fontsize', 20)
set(gca,'fontsize',12)

