""" Calling Weiwei + Yinghui's code """

import os

peer_dir = "/export/home/yh2639/pyramid/testdata/summary";
output_dir = "/export/home/yh2639/pyramid/test_output/peer";


### 1. extract peer summary
cm1 = "perl  new_merge_peers.pl  "+ peer_dir +" " + output_dir"/summary";
print "\n$cmd\n";
`$cmd`;

### 2. sort summary by id
$cmd = "sort  -k1,1 -k2n,2  $output_dir/summary  >  $output_dir/summary.st";
print "\n$cmd\n";
`$cmd`;

### 3. get text
$cmd = "cut  -f 4  $output_dir/summary.st  >  $output_dir/text";
print "\n$cmd\n";
`$cmd`;

### 4. tokenize
$cmd = "perl  tokenize_en.pl  $output_dir/text  $output_dir/text.tok";
print "\n$cmd\n";
`$cmd`;