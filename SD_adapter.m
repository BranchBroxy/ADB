function [spikepos]=SD_adapter(drcell_path, Selection, raw_data, sample_rate)
% remove old DrCell/Neuro/Cardio folder from search path
PathCell = textscan(path, '%s', 'Delimiter', pathsep);
PathCell = PathCell{1,1}; % unpack cell (as textscan was used);
for i=1:size(PathCell,1)
    if any(strfind(PathCell{i},'DrCell')) % remove all entries that contain string "DrCell"
        rmpath(PathCell{i});
    end
end

L = 10000; %Length of the signal
fs = 10000; %not to be change
numspikes = 50; %number of spikes (if this number is too large, with respect to L, then genMEASignal cannot place all spikes, resulting in an infinite loop)
sigma = 4; %determines SNR
% Add all DrCell folder to matlab search path
% path_full = mfilename('fullpath'); % get path of this m-file (.../path/DrCell.m)
path_full = drcell_path; % path of the main-folder (.../path/DrCell.m)
%disp(raw_data)
% disp(['Voller Path' path_full])
[path_drcell,~] = fileparts(path_full); % separate path and m-file-name

p=genpath(path_drcell); % get path of all subfolders
% disp(p)
addpath(p); % add to matlab search path

in.M = raw_data;
in.SaRa = sample_rate;

params.method = 'numspikes';
params.numspikes = numspikes;
params.filter = 0;

    if any(strcmp('ABS',Selection))
        disp('Getting Spikes with ABS');
        spikepos = ABS(in,params);
    end

    if any(strcmp('MTEO',Selection))
        disp('Getting Spikes with MTEO');
        spikepos = MTEO(in, [1 3 5], params);
    end

    if any(strcmp('PTSD',Selection))
        disp('Getting Spikes with PTSD');
        spikepos = PTSD(in,params);
    end

    if any(strcmp('SWT2012',Selection))
        disp('Getting Spikes with SWT2012');
        spikepos = SWT2012(in,params);
    end

    if any(strcmp('SWTEO',Selection))
        disp('Getting Spikes with SWTEO');
        spikepos = SWTTEO(in, params);
    end

    if any(strcmp('TIFCO',Selection))
        disp('Getting Spikes with TIFCO');
        spikepos = TIFCO(in,params);
    end

    if any(strcmp('WTEO',Selection))
        disp('Getting Spikes with WTEO');
        spikepos = WTEO(in,params);
    end

    if any(strcmp('genSpikes',Selection))
        disp('Generating Spikes');
        spikepos = genMEASignal(L,fs,sigma,numspikes,'randpos');
    end



end