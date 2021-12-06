# Various DPAT Outlier Dectection methods
- Dynamic Part Averaging Testing (DPAT)
- Automotive Electronics Council DPAT (AEC DPAT)
- Robust DPAT (R DPAT)

## DPAT
Dynamic Part Averaging Testing (DPAT) stands for 'Dynamic Part Average Testing'; the outlier thresholds are calculated for each wafer and test dynamically. Values outside the limits are considered outliers. 

<a href="https://www.codecogs.com/eqnedit.php?latex=Upper\_limit&space;=&space;median&space;&plus;&space;k&space;\times&space;stddev&space;\\&space;Lower\_limit&space;=&space;median&space;-&space;k&space;\times&space;stddev" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Upper\_limit&space;=&space;median&space;&plus;&space;k&space;\times&space;stddev&space;\\&space;Lower\_limit&space;=&space;median&space;-&space;k&space;\times&space;stddev" title="Upper\_limit = median + k \times stddev \\ Lower\_limit = median - k \times stddev" /></a>

## AEC DPAT
Automotive Electronics Council DPAT (AEC DPAT) is another version of DPAT. They way of computing the upper and lower threshold is different from the original DPAT.

<a href="https://www.codecogs.com/eqnedit.php?latex=Upper\_limit&space;=&space;median&space;&plus;&space;k&space;\times&space;(p99-median)&space;\times&space;0.43&space;\\&space;Lower\_limit&space;=&space;median&space;-&space;k&space;\times&space;(median-p1)&space;\times&space;0.43" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Upper\_limit&space;=&space;median&space;&plus;&space;k&space;\times&space;(p99-median)&space;\times&space;0.43&space;\\&space;Lower\_limit&space;=&space;median&space;-&space;k&space;\times&space;(median-p1)&space;\times&space;0.43" title="Upper\_limit = median + k \times (p99-median) \times 0.43 \\ Lower\_limit = median - k \times (median-p1) \times 0.43" /></a>

## R DPAT
Robust DPAR (R DPAT) is a variation of the original DPAT. The method includes 1) transforming non-normal data to normal, which makes DPAT robust to the skewness of the distribution, and 2) using robust statistics, Grubbs algorithm, which is robust to the dispersion estimation. The following steps are the detailed algorithm of R DPAT:

1. The Anbderson Darling test is applied to test the normality of data.
2. If the distribution is not normal, the Grubbs algorithm is applied recursively to remove all the outliers to make the distribution normal.
3. If the resulting distribution is not normal, a Johnson transformation is applied.
4. If the tranformed distribution is normal, the Grubbs algorithm is applied and the algorithm ends.
5. If the transformed distribution is non-normal, the AEC DPAT is applied to the original data set.
