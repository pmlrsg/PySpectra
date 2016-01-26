import unittest
import os

import numpy as np
from numpy.testing import assert_allclose

from PySpectra import extract_spectra_from_file

TEST_INPUTS_DIRECTORY = os.path.join(os.path.dirname(__file__), 'inputs')

class USGSTests(unittest.TestCase):

    correct_wavelengths = np.array([
           339.600006,  341.100006,  342.600006,  344.100006,  345.500000,
           347.000000,  348.500000,  350.000000,  351.399994,  352.899994,
           354.399994,  355.799988,  357.299988,  358.799988,  360.200012,
           361.700012,  363.200012,  364.700012,  366.100006,  367.600006,
           369.100006,  370.500000,  372.000000,  373.500000,  374.899994,
           376.399994,  377.899994,  379.299988,  380.799988,  382.299988,
           383.700012,  385.200012,  386.700012,  388.100006,  389.600006,
           391.100006,  392.500000,  394.000000,  395.500000,  396.899994,
           398.399994,  399.799988,  401.299988,  402.799988,  404.200012,
           405.700012,  407.100006,  408.600006,  410.000000,  411.500000,
           413.000000,  414.399994,  415.899994,  417.299988,  418.799988,
           420.200012,  421.700012,  423.100006,  424.600006,  426.000000,
           427.500000,  428.899994,  430.399994,  431.799988,  433.299988,
           434.700012,  436.100006,  437.600006,  439.000000,  440.500000,
           441.899994,  443.399994,  444.799988,  446.200012,  447.700012,
           449.100006,  450.600006,  452.000000,  453.399994,  454.899994,
           456.299988,  457.700012,  459.200012,  460.600006,  462.000000,
           463.500000,  464.899994,  466.299988,  467.799988,  469.200012,
           470.600006,  472.000000,  473.500000,  474.899994,  476.299988,
           477.799988,  479.200012,  480.600006,  482.000000,  483.500000,
           484.899994,  486.299988,  487.700012,  489.100006,  490.500000,
           492.000000,  493.399994,  494.799988,  496.200012,  497.600006,
           499.000000,  500.500000,  501.899994,  503.299988,  504.700012,
           506.100006,  507.500000,  508.899994,  510.299988,  511.799988,
           513.200012,  514.599976,  516.000000,  517.400024,  518.799988,
           520.200012,  521.599976,  523.000000,  524.400024,  525.799988,
           527.200012,  528.599976,  530.000000,  531.400024,  532.799988,
           534.200012,  535.599976,  537.000000,  538.400024,  539.799988,
           541.200012,  542.599976,  544.000000,  545.299988,  546.700012,
           548.099976,  549.500000,  550.900024,  552.299988,  553.700012,
           555.099976,  556.500000,  557.799988,  559.200012,  560.599976,
           562.000000,  563.400024,  564.799988,  566.200012,  567.500000,
           568.900024,  570.299988,  571.700012,  573.099976,  574.400024,
           575.799988,  577.200012,  578.599976,  580.000000,  581.299988,
           582.700012,  584.099976,  585.500000,  586.799988,  588.200012,
           589.599976,  591.000000,  592.299988,  593.700012,  595.099976,
           596.400024,  597.799988,  599.200012,  600.500000,  601.900024,
           603.299988,  604.700012,  606.000000,  607.400024,  608.799988,
           610.099976,  611.500000,  612.799988,  614.200012,  615.599976,
           616.900024,  618.299988,  619.700012,  621.000000,  622.400024,
           623.700012,  625.099976,  626.400024,  627.799988,  629.200012,
           630.500000,  631.900024,  633.200012,  634.599976,  635.900024,
           637.299988,  638.599976,  640.000000,  641.299988,  642.700012,
           644.000000,  645.400024,  646.700012,  648.099976,  649.400024,
           650.799988,  652.099976,  653.500000,  654.799988,  656.200012,
           657.500000,  658.900024,  660.200012,  661.500000,  662.900024,
           664.200012,  665.599976,  666.900024,  668.200012,  669.599976,
           670.900024,  672.299988,  673.599976,  674.900024,  676.299988,
           677.599976,  679.000000,  680.299988,  681.599976,  683.000000,
           684.299988,  685.599976,  686.900024,  688.299988,  689.599976,
           690.900024,  692.299988,  693.599976,  694.900024,  696.200012,
           697.599976,  698.900024,  700.200012,  701.500000,  702.900024,
           704.200012,  705.500000,  706.799988,  708.099976,  709.500000,
           710.799988,  712.099976,  713.400024,  714.700012,  716.000000,
           717.400024,  718.700012,  720.000000,  721.299988,  722.599976,
           723.900024,  725.200012,  726.500000,  727.799988,  729.200012,
           730.500000,  731.799988,  733.099976,  734.400024,  735.700012,
           737.000000,  738.299988,  739.599976,  740.900024,  742.200012,
           743.500000,  744.799988,  746.099976,  747.400024,  748.700012,
           750.000000,  751.200012,  752.500000,  753.799988,  755.099976,
           756.400024,  757.700012,  759.000000,  760.299988,  761.599976,
           762.799988,  764.099976,  765.400024,  766.700012,  768.000000,
           769.200012,  770.500000,  771.799988,  773.099976,  774.400024,
           775.599976,  776.900024,  778.200012,  779.500000,  780.700012,
           782.000000,  783.299988,  784.500000,  785.799988,  787.099976,
           788.299988,  789.599976,  790.900024,  792.099976,  793.400024,
           794.599976,  795.900024,  797.200012,  798.400024,  799.700012,
           800.900024,  802.200012,  803.400024,  804.700012,  805.900024,
           807.200012,  808.400024,  809.700012,  810.900024,  812.200012,
           813.400024,  814.599976,  815.900024,  817.099976,  818.400024,
           819.599976,  820.799988,  822.099976,  823.299988,  824.500000,
           825.799988,  827.000000,  828.200012,  829.500000,  830.700012,
           831.900024,  833.099976,  834.299988,  835.599976,  836.799988,
           838.000000,  839.200012,  840.400024,  841.700012,  842.900024,
           844.099976,  845.299988,  846.500000,  847.700012,  848.900024,
           850.099976,  851.299988,  852.500000,  853.799988,  855.000000,
           856.200012,  857.400024,  858.500000,  859.799988,  861.000000,
           862.099976,  863.299988,  864.500000,  865.700012,  866.900024,
           868.099976,  869.299988,  870.500000,  871.700012,  872.799988,
           874.000000,  875.200012,  876.400024,  877.599976,  878.799988,
           879.900024,  881.099976,  882.299988,  883.500000,  884.599976,
           885.799988,  887.000000,  888.200012,  889.299988,  890.500000,
           891.700012,  892.799988,  894.000000,  895.200012,  896.299988,
           897.500000,  898.599976,  899.799988,  901.000000,  902.099976,
           903.299988,  904.400024,  905.599976,  906.700012,  907.900024,
           909.000000,  910.200012,  911.299988,  912.500000,  913.599976,
           914.799988,  915.900024,  917.099976,  918.200012,  919.400024,
           920.500000,  921.700012,  922.799988,  924.000000,  925.099976,
           926.200012,  927.400024,  928.500000,  929.700012,  930.799988,
           931.900024,  933.099976,  934.200012,  935.299988,  936.500000,
           937.599976,  938.799988,  939.900024,  941.000000,  942.200012,
           943.299988,  944.400024,  945.599976,  946.700012,  947.799988,
           949.000000,  950.099976,  951.200012,  952.299988,  953.500000,
           954.599976,  955.799988,  956.900024,  958.000000,  959.200012,
           960.299988,  961.400024,  962.500000,  963.700012,  964.799988,
           966.000000,  967.099976,  968.200012,  969.400024,  970.500000,
           971.599976,  972.799988,  973.900024,  975.000000,  976.200012,
           977.299988,  978.500000,  979.599976,  980.799988,  981.900024,
           983.000000,  984.200012,  985.299988,  986.500000,  987.599976,
           988.799988,  989.900024,  991.099976,  992.200012,  993.400024,
           994.500000,  995.700012,  996.900024,  998.000000,  999.200012,
           1000.299988,  1001.500000,  1002.700012,  1003.799988,  1005.000000, 
           1006.200012,  1007.400024,  970.799988,  974.599976,  978.500000,
           982.299988,  986.099976,  989.900024,  993.700012,  997.500000,
           1001.299988,  1005.099976,  1008.900024,  1012.700012,  1016.500000,
           1020.299988,  1024.199951,  1028.000000,  1031.800049,  1035.599976,
           1039.400024,  1043.199951,  1047.000000,  1050.800049,  1054.599976,
           1058.400024,  1062.199951,  1066.000000,  1069.800049,  1073.599976,
           1077.400024,  1081.199951,  1085.000000,  1088.800049,  1092.599976,
           1096.400024,  1100.199951,  1104.000000,  1107.800049,  1111.599976,
           1115.400024,  1119.199951,  1122.900024,  1126.699951,  1130.500000,
           1134.300049,  1138.099976,  1141.900024,  1145.699951,  1149.500000,
           1153.300049,  1157.000000,  1160.800049,  1164.599976,  1168.400024,
           1172.199951,  1176.000000,  1179.699951,  1183.500000,  1187.300049,
           1191.099976,  1194.800049,  1198.599976,  1202.400024,  1206.199951,
           1209.900024,  1213.699951,  1217.500000,  1221.300049,  1225.000000,
           1228.800049,  1232.599976,  1236.300049,  1240.099976,  1243.900024,
           1247.599976,  1251.400024,  1255.199951,  1258.900024,  1262.699951,
           1266.400024,  1270.199951,  1274.000000,  1277.699951,  1281.500000,
           1285.199951,  1289.000000,  1292.699951,  1296.500000,  1300.199951,
           1304.000000,  1307.699951,  1311.500000,  1315.199951,  1319.000000,
           1322.699951,  1326.500000,  1330.199951,  1333.900024,  1337.699951,
           1341.400024,  1345.199951,  1348.900024,  1352.599976,  1356.400024,
           1360.099976,  1363.800049,  1367.599976,  1371.300049,  1375.000000,
           1378.800049,  1382.500000,  1386.199951,  1389.900024,  1393.599976,
           1397.400024,  1401.099976,  1404.800049,  1408.500000,  1412.199951,
           1415.900024,  1419.699951,  1423.400024,  1427.099976,  1430.800049,
           1434.500000,  1438.199951,  1441.900024,  1445.599976,  1449.300049,
           1453.000000,  1456.699951,  1460.400024,  1464.099976,  1467.800049,
           1471.500000,  1475.199951,  1478.800049,  1482.500000,  1486.199951,
           1489.900024,  1493.599976,  1497.300049,  1500.900024,  1504.599976,
           1508.300049,  1512.000000,  1515.699951,  1519.300049,  1523.000000,
           1526.699951,  1530.300049,  1534.000000,  1537.699951,  1541.300049,
           1545.000000,  1548.699951,  1552.300049,  1556.000000,  1559.599976,
           1563.300049,  1566.900024,  1570.599976,  1574.199951,  1577.900024,
           1581.500000,  1585.199951,  1588.800049,  1592.400024,  1596.099976,
           1599.699951,  1603.300049,  1607.000000,  1610.599976,  1614.199951,
           1617.800049,  1621.500000,  1625.099976,  1628.699951,  1632.300049,
           1636.000000,  1639.599976,  1643.199951,  1646.800049,  1650.400024,
           1654.000000,  1657.599976,  1661.199951,  1664.800049,  1668.400024,
           1672.000000,  1675.599976,  1679.199951,  1682.800049,  1686.400024,
           1690.000000,  1693.599976,  1697.199951,  1700.800049,  1704.300049,
           1707.900024,  1711.500000,  1715.099976,  1718.599976,  1722.199951,
           1725.800049,  1729.300049,  1732.900024,  1736.500000,  1740.000000,
           1743.599976,  1747.099976,  1750.699951,  1754.199951,  1757.800049,
           1761.300049,  1764.900024,  1768.400024,  1772.000000,  1775.500000,
           1779.099976,  1782.599976,  1786.099976,  1789.599976,  1793.199951,
           1796.699951,  1800.199951,  1803.699951,  1807.300049,  1810.800049,
           1814.300049,  1817.800049,  1821.300049,  1824.800049,  1828.300049,
           1831.800049,  1835.300049,  1838.800049,  1842.300049,  1845.800049,
           1849.300049,  1852.800049,  1856.300049,  1859.800049,  1863.199951,
           1866.699951,  1870.199951,  1873.699951,  1877.199951,  1880.599976,
           1884.099976,  1887.599976,  1891.000000,  1894.500000,  1898.599976,
           1901.300049,  1904.000000,  1906.699951,  1909.400024,  1912.099976,
           1914.800049,  1917.500000,  1920.199951,  1922.800049,  1925.500000,
           1928.199951,  1930.900024,  1933.599976,  1936.300049,  1938.900024,
           1941.599976,  1944.300049,  1946.900024,  1949.599976,  1952.300049,
           1954.900024,  1957.599976,  1960.199951,  1962.900024,  1965.599976,
           1968.199951,  1970.900024,  1973.500000,  1976.199951,  1978.800049,
           1981.400024,  1984.099976,  1986.699951,  1989.300049,  1992.000000,
           1994.599976,  1997.199951,  1999.900024,  2002.500000,  2005.099976,
           2007.699951,  2010.300049,  2012.900024,  2015.599976,  2018.199951,
           2020.800049,  2023.400024,  2026.000000,  2028.599976,  2031.199951,
           2033.800049,  2036.400024,  2039.000000,  2041.599976,  2044.199951,
           2046.699951,  2049.300049,  2051.899902,  2054.500000,  2057.100098,
           2059.600098,  2062.199951,  2064.800049,  2067.399902,  2069.899902,
           2072.500000,  2075.100098,  2077.600098,  2080.199951,  2082.699951,
           2085.300049,  2087.800049,  2090.399902,  2092.899902,  2095.500000,
           2098.000000,  2100.600098,  2103.100098,  2105.600098,  2108.199951,
           2110.699951,  2113.199951,  2115.800049,  2118.300049,  2120.800049,
           2123.300049,  2125.899902,  2128.399902,  2130.899902,  2133.399902,
           2135.899902,  2138.399902,  2140.899902,  2143.399902,  2145.899902,
           2148.399902,  2150.899902,  2153.399902,  2155.899902,  2158.399902,
           2160.899902,  2163.399902,  2165.899902,  2168.399902,  2170.800049,
           2173.300049,  2175.800049,  2178.300049,  2180.800049,  2183.199951,
           2185.699951,  2188.100098,  2190.600098,  2193.100098,  2195.500000,
           2198.000000,  2200.399902,  2202.899902,  2205.399902,  2207.800049,
           2210.199951,  2212.699951,  2215.100098,  2217.600098,  2220.000000,
           2222.399902,  2224.899902,  2227.300049,  2229.699951,  2232.199951,
           2234.600098,  2237.000000,  2239.399902,  2241.899902,  2244.300049,
           2246.699951,  2249.100098,  2251.500000,  2253.899902,  2256.300049,
           2258.699951,  2261.100098,  2263.500000,  2265.899902,  2268.300049,
           2270.699951,  2273.100098,  2275.500000,  2277.899902,  2280.300049,
           2282.600098,  2285.000000,  2287.399902,  2289.800049,  2292.100098,
           2294.500000,  2296.899902,  2299.199951,  2301.600098,  2304.000000,
           2306.300049,  2308.699951,  2311.100098,  2313.399902,  2315.800049,
           2318.100098,  2320.500000,  2322.800049,  2325.100098,  2327.500000,
           2329.800049,  2332.199951,  2334.500000,  2336.800049,  2339.199951,
           2341.500000,  2343.800049,  2346.100098,  2348.500000,  2350.800049,
           2353.100098,  2355.399902,  2357.699951,  2360.000000,  2362.300049,
           2364.600098,  2366.899902,  2369.199951,  2371.600098,  2373.899902,
           2376.100098,  2378.399902,  2380.699951,  2383.000000,  2385.300049,
           2387.600098,  2389.899902,  2392.199951,  2394.399902,  2396.699951,
           2399.000000,  2401.300049,  2403.500000,  2405.800049,  2408.100098,
           2410.300049,  2412.600098,  2414.800049,  2417.100098,  2419.399902,
           2421.600098,  2423.899902,  2426.100098,  2428.399902,  2430.600098,
           2432.800049,  2435.100098,  2437.300049,  2439.600098,  2441.800049,
           2444.000000,  2446.199951,  2448.500000,  2450.699951,  2452.899902,
           2455.100098,  2457.399902,  2459.600098,  2461.800049,  2464.000000,
           2466.199951,  2468.399902,  2470.600098,  2472.800049,  2475.000000,
           2477.199951,  2479.399902,  2481.600098,  2483.800049,  2486.000000,
           2488.199951,  2490.399902,  2492.600098,  2494.699951,  2496.899902,
           2499.100098,  2501.300049,  2503.399902,  2505.600098,  2507.800049,
           2509.899902,  2512.100098,  2514.300049,  2516.399902,  2518.600098])

    correct_values = np.array([
                        0.0265,  0.0266,  0.0199,  0.0227,  0.0208,  0.0173,
                        0.0153,  0.0144,  0.0132,  0.0121,  0.0114,  0.0120,
                        0.0114,  0.0100,  0.0093,  0.0094,  0.0100,  0.0097,
                        0.0090,  0.0089,  0.0093,  0.0099,  0.0092,  0.0098,
                        0.0089,  0.0095,  0.0092,  0.0097,  0.0093,  0.0098,
                        0.0106,  0.0098,  0.0101,  0.0103,  0.0105,  0.0108,
                        0.0114,  0.0114,  0.0117,  0.0115,  0.0114,  0.0115,
                        0.0115,  0.0119,  0.0120,  0.0121,  0.0124,  0.0127,
                        0.0131,  0.0135,  0.0137,  0.0138,  0.0142,  0.0144,
                        0.0143,  0.0144,  0.0147,  0.0149,  0.0149,  0.0152,
                        0.0155,  0.0156,  0.0159,  0.0158,  0.0159,  0.0161,
                        0.0162,  0.0163,  0.0165,  0.0166,  0.0167,  0.0169,
                        0.0172,  0.0174,  0.0177,  0.0179,  0.0181,  0.0182,
                        0.0184,  0.0187,  0.0189,  0.0190,  0.0192,  0.0193,
                        0.0194,  0.0195,  0.0196,  0.0197,  0.0198,  0.0199,
                        0.0201,  0.0201,  0.0203,  0.0205,  0.0206,  0.0208,
                        0.0209,  0.0210,  0.0211,  0.0213,  0.0215,  0.0216,
                        0.0218,  0.0220,  0.0223,  0.0226,  0.0229,  0.0233,
                        0.0237,  0.0242,  0.0247,  0.0253,  0.0261,  0.0269,
                        0.0278,  0.0288,  0.0300,  0.0313,  0.0327,  0.0342,
                        0.0359,  0.0378,  0.0398,  0.0420,  0.0443,  0.0466,
                        0.0489,  0.0512,  0.0533,  0.0555,  0.0578,  0.0599,
                        0.0617,  0.0635,  0.0651,  0.0665,  0.0677,  0.0689,
                        0.0700,  0.0710,  0.0718,  0.0726,  0.0734,  0.0741,
                        0.0747,  0.0755,  0.0761,  0.0766,  0.0772,  0.0776,
                        0.0777,  0.0776,  0.0773,  0.0770,  0.0766,  0.0760,
                        0.0753,  0.0745,  0.0736,  0.0726,  0.0715,  0.0703,
                        0.0691,  0.0679,  0.0668,  0.0657,  0.0648,  0.0639,
                        0.0631,  0.0624,  0.0618,  0.0611,  0.0606,  0.0601,
                        0.0597,  0.0593,  0.0589,  0.0586,  0.0584,  0.0582,
                        0.0581,  0.0580,  0.0578,  0.0576,  0.0575,  0.0572,
                        0.0570,  0.0566,  0.0562,  0.0557,  0.0552,  0.0547,
                        0.0541,  0.0536,  0.0530,  0.0526,  0.0520,  0.0517,
                        0.0514,  0.0511,  0.0509,  0.0508,  0.0508,  0.0508,
                        0.0507,  0.0507,  0.0506,  0.0504,  0.0501,  0.0497,
                        0.0491,  0.0485,  0.0478,  0.0470,  0.0461,  0.0453,
                        0.0445,  0.0437,  0.0431,  0.0425,  0.0420,  0.0416,
                        0.0414,  0.0410,  0.0407,  0.0402,  0.0397,  0.0390,
                        0.0384,  0.0377,  0.0370,  0.0365,  0.0360,  0.0355,
                        0.0352,  0.0350,  0.0349,  0.0348,  0.0348,  0.0349,
                        0.0352,  0.0355,  0.0360,  0.0367,  0.0376,  0.0389,
                        0.0409,  0.0436,  0.0469,  0.0507,  0.0550,  0.0598,
                        0.0656,  0.0721,  0.0790,  0.0864,  0.0942,  0.1026,
                        0.1110,  0.1195,  0.1278,  0.1360,  0.1441,  0.1523,
                        0.1605,  0.1687,  0.1769,  0.1850,  0.1931,  0.2013,
                        0.2102,  0.2199,  0.2295,  0.2383,  0.2469,  0.2555,
                        0.2644,  0.2733,  0.2819,  0.2904,  0.2984,  0.3061,
                        0.3135,  0.3203,  0.3268,  0.3330,  0.3389,  0.3445,
                        0.3495,  0.3542,  0.3586,  0.3626,  0.3662,  0.3695,
                        0.3725,  0.3753,  0.3778,  0.3801,  0.3821,  0.3839,
                        0.3855,  0.3872,  0.3890,  0.3910,  0.3926,  0.3936,
                        0.3943,  0.3950,  0.3957,  0.3966,  0.3975,  0.3983,
                        0.3992,  0.4000,  0.4007,  0.4015,  0.4022,  0.4028,
                        0.4037,  0.4044,  0.4050,  0.4057,  0.4065,  0.4071,
                        0.4077,  0.4085,  0.4092,  0.4099,  0.4105,  0.4111,
                        0.4117,  0.4124,  0.4129,  0.4137,  0.4144,  0.4152,
                        0.4157,  0.4162,  0.4169,  0.4178,  0.4183,  0.4190,
                        0.4195,  0.4200,  0.4205,  0.4213,  0.4218,  0.4220,
                        0.4224,  0.4229,  0.4238,  0.4243,  0.4249,  0.4253,
                        0.4259,  0.4264,  0.4269,  0.4274,  0.4277,  0.4284,
                        0.4289,  0.4291,  0.4295,  0.4302,  0.4311,  0.4317,
                        0.4319,  0.4324,  0.4327,  0.4336,  0.4341,  0.4347,
                        0.4349,  0.4353,  0.4361,  0.4367,  0.4368,  0.4377,
                        0.4376,  0.4380,  0.4389,  0.4396,  0.4396,  0.4404,
                        0.4406,  0.4410,  0.4414,  0.4419,  0.4425,  0.4429,
                        0.4434,  0.4437,  0.4439,  0.4444,  0.4452,  0.4452,
                        0.4458,  0.4462,  0.4466,  0.4466,  0.4471,  0.4479,
                        0.4482,  0.4481,  0.4484,  0.4490,  0.4494,  0.4496,
                        0.4496,  0.4497,  0.4504,  0.4501,  0.4500,  0.4498,
                        0.4507,  0.4503,  0.4495,  0.4500,  0.4502,  0.4515,
                        0.4521,  0.4529,  0.4523,  0.4521,  0.4520,  0.4517,
                        0.4512,  0.4522,  0.4525,  0.4531,  0.4532,  0.4533,
                        0.4534,  0.4526,  0.4539,  0.4538,  0.4541,  0.4551,
                        0.4534,  0.4532,  0.4513,  0.4518,  0.4519,  0.4491,
                        0.4456,  0.4407,  0.4409,  0.4367,  0.4376,  0.4359,
                        0.4393,  0.4417,  0.4412,  0.4379,  0.4370,  0.4347,
                        0.4346,  0.4394,  0.4361,  0.4305,  0.4297,  0.4310,
                        0.4279,  0.4305,  0.4283,  0.4284,  0.4273,  0.4261,
                        0.4218,  0.4238,  0.4248,  0.4224,  0.4233,  0.4231,
                        0.4218,  0.4242,  0.4246,  0.4250,  0.4256,  0.4250,
                        0.4283,  0.4262,  0.4260,  0.4233,  0.4225,  0.4257,
                        0.4278,  0.4237,  0.4234,  0.4221,  0.4232,  0.4223,
                        0.4231,  0.4234,  0.4242,  0.4237,  0.4261,  0.4259,
                        0.4252,  0.4260,  0.4296,  0.4295,  0.4297,  0.4321,
                        0.4327,  0.4330,  0.4361,  0.4361,  0.4361,  0.4361,
                        0.4391,  0.4391,  0.4263,  0.4245,  0.4252,  0.4227,
                        0.4232,  0.4247,  0.4276,  0.4309,  0.4345,  0.4377,
                        0.4405,  0.4434,  0.4467,  0.4496,  0.4527,  0.4556,
                        0.4580,  0.4605,  0.4628,  0.4651,  0.4668,  0.4684,
                        0.4697,  0.4709,  0.4720,  0.4732,  0.4741,  0.4750,
                        0.4757,  0.4760,  0.4761,  0.4757,  0.4751,  0.4741,
                        0.4724,  0.4704,  0.4682,  0.4655,  0.4618,  0.4569,
                        0.4511,  0.4443,  0.4388,  0.4335,  0.4272,  0.4191,
                        0.4088,  0.4005,  0.3946,  0.3903,  0.3877,  0.3866,
                        0.3861,  0.3862,  0.3862,  0.3863,  0.3860,  0.3856,
                        0.3854,  0.3854,  0.3857,  0.3863,  0.3874,  0.3890,
                        0.3904,  0.3919,  0.3938,  0.3961,  0.3982,  0.4007,
                        0.4028,  0.4047,  0.4065,  0.4083,  0.4098,  0.4111,
                        0.4122,  0.4132,  0.4137,  0.4138,  0.4136,  0.4129,
                        0.4121,  0.4110,  0.4089,  0.4071,  0.4042,  0.4006,
                        0.3963,  0.3909,  0.3849,  0.3778,  0.3706,  0.3638,
                        0.3571,  0.3495,  0.3414,  0.3343,  0.3288,  0.3251,
                        0.3228,  0.3185,  0.3127,  0.3009,  0.3007,  0.3051,
                        0.3005,  0.3042,  0.2957,  0.2907,  0.2816,  0.2670,
                        0.2651,  0.2562,  0.2500,  0.2283,  0.2095,  0.1839,
                        0.1611,  0.1430,  0.1279,  0.1199,  0.1140,  0.1121,
                        0.1090,  0.1027,  0.0969,  0.0926,  0.0897,  0.0879,
                        0.0882,  0.0906,  0.0921,  0.0939,  0.0947,  0.0962,
                        0.0971,  0.0983,  0.0991,  0.1009,  0.1029,  0.1054,
                        0.1083,  0.1111,  0.1140,  0.1172,  0.1207,  0.1240,
                        0.1270,  0.1302,  0.1335,  0.1368,  0.1399,  0.1431,
                        0.1462,  0.1495,  0.1526,  0.1555,  0.1585,  0.1614,
                        0.1645,  0.1673,  0.1700,  0.1727,  0.1752,  0.1782,
                        0.1806,  0.1832,  0.1859,  0.1883,  0.1909,  0.1932,
                        0.1955,  0.1978,  0.2000,  0.2021,  0.2042,  0.2058,
                        0.2076,  0.2091,  0.2109,  0.2120,  0.2131,  0.2141,
                        0.2149,  0.2156,  0.2163,  0.2169,  0.2169,  0.2167,
                        0.2164,  0.2158,  0.2152,  0.2143,  0.2131,  0.2120,
                        0.2110,  0.2099,  0.2088,  0.2074,  0.2058,  0.2043,
                        0.2027,  0.2011,  0.1996,  0.1981,  0.1965,  0.1948,
                        0.1926,  0.1905,  0.1880,  0.1855,  0.1833,  0.1812,
                        0.1801,  0.1784,  0.1772,  0.1762,  0.1758,  0.1756,
                        0.1758,  0.1768,  0.1793,  0.1818,  0.1863,  0.1967,
                        0.2068,  0.2191,  0.2319,  0.2423,  0.2546,  0.2629,
                        0.2759,  0.2937,  0.2927,  0.2899,  0.3113,  0.3000,
                        0.3079,  0.3155,  0.2914,  0.3000,  0.2798,  0.2805,
                        0.3000,  0.2927,  0.2964,  0.3049,  0.3049,  0.3074,
                        0.2951,  0.3240,  0.2353,  0.1053,  0.0976,  0.0714,
                        0.0769,  0.0526,  0.0732,  0.0889,  0.0455,  0.0667,
                        0.1111,  0.1148,  0.1029,  0.0959,  0.0633,  0.0417,
                        0.0308,  0.0225,  0.0335,  0.0358,  0.0375,  0.0400,
                        0.0424,  0.0358,  0.0359,  0.0373,  0.0338,  0.0315,
                        0.0308,  0.0310,  0.0321,  0.0328,  0.0337,  0.0349,
                        0.0343,  0.0342,  0.0366,  0.0388,  0.0377,  0.0394,
                        0.0415,  0.0401,  0.0426,  0.0417,  0.0418,  0.0458,
                        0.0460,  0.0471,  0.0481,  0.0474,  0.0482,  0.0502,
                        0.0510,  0.0515,  0.0526,  0.0523,  0.0520,  0.0533,
                        0.0549,  0.0560,  0.0547,  0.0554,  0.0576,  0.0574,
                        0.0564,  0.0579,  0.0595,  0.0601,  0.0608,  0.0622,
                        0.0632,  0.0642,  0.0649,  0.0656,  0.0663,  0.0667,
                        0.0678,  0.0688,  0.0694,  0.0708,  0.0717,  0.0727,
                        0.0733,  0.0744,  0.0760,  0.0764,  0.0765,  0.0774,
                        0.0778,  0.0787,  0.0797,  0.0806,  0.0820,  0.0824,
                        0.0827,  0.0840,  0.0845,  0.0844,  0.0851,  0.0863,
                        0.0875,  0.0885,  0.0884,  0.0891,  0.0906,  0.0911,
                        0.0915,  0.0915,  0.0925,  0.0932,  0.0936,  0.0952,
                        0.0959,  0.0965,  0.0977,  0.0985,  0.0985,  0.0993,
                        0.1002,  0.1003,  0.0995,  0.0996,  0.0999,  0.0987,
                        0.0978,  0.0976,  0.0963,  0.0958,  0.0960,  0.0953,
                        0.0945,  0.0940,  0.0930,  0.0928,  0.0921,  0.0910,
                        0.0902,  0.0882,  0.0870,  0.0870,  0.0859,  0.0850,
                        0.0841,  0.0832,  0.0821,  0.0809,  0.0804,  0.0795,
                        0.0772,  0.0779,  0.0774,  0.0761,  0.0759,  0.0747,
                        0.0735,  0.0730,  0.0738,  0.0732,  0.0706,  0.0706,
                        0.0695,  0.0680,  0.0675,  0.0671,  0.0664,  0.0654,
                        0.0651,  0.0648,  0.0647,  0.0647,  0.0650,  0.0647,
                        0.0615,  0.0613,  0.0614,  0.0592,  0.0609,  0.0613,
                        0.0608,  0.0622,  0.0594,  0.0556,  0.0553,  0.0575,
                        0.0556,  0.0534,  0.0533,  0.0537,  0.0516,  0.0515,
                        0.0510,  0.0509,  0.0507,  0.0509,  0.0507,  0.0511,
                        0.0486,  0.0485,  0.0522,  0.0489,  0.0451,  0.0465,
                        0.0497,  0.0489,  0.0476,  0.0451,  0.0444,  0.0469,
                        0.0489,  0.0447,  0.0392,  0.0428,  0.0409,  0.0389,
                        0.0391,  0.0397,  0.0380,  0.0356,  0.0378,  0.0382,
                        0.0369,  0.0353,  0.0371,  0.0361,  0.0345,  0.0347,
                        0.0372,  0.0342,  0.0331,  0.0330,  0.0314,  0.0381,
                        0.0440,  0.0449,  0.0456,  0.0435,  0.0428,  0.0481,
                        0.0526,  0.0561,  0.0724,  0.0726,  0.0545,  0.0660,
                        0.0943,  0.0826,  0.0424,  0.0480,  0.0661,  0.0270,
                        0.0515,  0.0714,  0.0571,  0.0328,  0.0377,  0.2391])

    def test_read_sig_file(self):
        s = extract_spectra_from_file(os.path.join(TEST_INPUTS_DIRECTORY,
                                                   "wyken1_049.sig"),
                                                   "sig")

        assert_allclose(s.wavelengths, self.correct_wavelengths)
        assert_allclose(s.values, self.correct_values)

