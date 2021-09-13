## tokenizer
-------
1. - [ ] kmp search based start index & end index
2. - [ ] traceback original text ( or decode )
3. - [ ] doc_stride provide
4. ~~- [ ] tokenizer adapted join~~
> ### multi answer 구현
> ---------
> 1. context에서 answer string matching 
> 2. char index to input ids candidate 구함
> 3. question + context 에서 input ids 매칭
> ### 

## dataloader
-----
1. control by tokenizer
2. dynamic padding, batchsize
3. batchsize * padding ^ 2 <= min batchsize * max padding ^ 2
4. args: (dataset, max_padding = 384, min_batchsize = 8, Pmul = 64, Bmul = None)# None은 static 하게 사용됨을 의미
> ### 구현
> -------------
> 1. pad 길이 역정렬
> 2. sample pool 부족시 index늘리기 (항상 부족할것 임)
> 2. sample 가능한 목록중 최대길이의 항목은 무조건 사용
> 3. 가장 긴 항목 기준으로 다룰 수 있는 최대 Batchsize 결정
> 4. Batchsize 만큼 sampling ( 가장 긴 pad항목 포함 )
> 5. 적합한 padding 결정후 crop