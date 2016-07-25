function [ res ] = normalize( v )
%NORMALIZE Summary of this function goes here
%   Detailed explanation goes here

res = v / norm(v, 1);

end

