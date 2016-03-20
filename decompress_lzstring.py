keyStrBase64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
keyStrUriSafe = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-$"
baseReverseDic = {}

def getBaseValue(alphabet, character):
  if alphabet not in baseReverseDic:
    baseReverseDic[alphabet] = {}
    for i in range(len(alphabet)):
      baseReverseDic[alphabet][alphabet[i]] = i
  return baseReverseDic[alphabet][character]

def decompressFromEncodedURIComponent(input):
  if input == None:
    return ''
  if input == '':
    return ''
  input = input.replace(' ', '+')
  def index_to_base_value(index):
    return getBaseValue(keyStrUriSafe, input[index])
  return lzdecompress(len(input), 32, index_to_base_value)

def decompressFromBase64(input):
  if input == None:
    return ''
  if input == '':
    return ''
  def index_to_base_value(index):
    return getBaseValue(keyStrBase64, input[index])
  return lzdecompress(len(input), 32, index_to_base_value)

def one_if_greater_than_zero(val):
  if val > 0:
    return 1
  return 0

def assign_array(arr, idx, val):
  while len(arr) < idx+1:
    arr.append(0)
  arr[idx] = val

def lzdecompress(length, resetValue, getNextValue):
  dictionary = []
  next = 0
  enlargeIn = 4
  dictSize = 4
  numBits = 3
  entry = ''
  result = []
  i = 0
  w = 0
  bits = 0
  resb = 0
  maxpower = 0
  power = 0
  c = 0
  data = {
    'val': getNextValue(0),
    'position': resetValue,
    'index': 1
  }
  for i in range(3):
    assign_array(dictionary, i, i)
  bits = 0
  maxpower = pow(2, 2)
  power = 1
  while power != maxpower:
    resb = data['val'] & data['position']
    data['position'] >>= 1
    if data['position'] == 0:
      data['position'] = resetValue
      data['val'] = getNextValue(data['index'])
      data['index'] += 1
    bits |= one_if_greater_than_zero(resb) * power
    power <<= 1
  
  next = bits
  if next == 0:
    bits = 0
    maxpower = pow(2, 8)
    power = 1
    while power != maxpower:
      resb = data['val'] & data['position']
      data['position'] >>= 1
      if data['position'] == 0:
        data['position'] = resetValue
        data['val'] = getNextValue(data['index'])
        data['index'] += 1
      bits |= one_if_greater_than_zero(resb) * power
      power <<= 1
    c = unichr(bits)
  elif next == 1:
    bits = 0
    maxpower = pow(2, 16)
    power = 1
    while power != maxpower:
      resb = data['val'] & data['position']
      data['position'] >>= 1
      if data['position'] == 0:
        data['position'] = resetValue
        data['val'] = getNextValue(data['index'])
        data['index'] += 1
      bits |= one_if_greater_than_zero(resb) * power
      power <<= 1
    c = unichr(bits)
  elif next == 2:
    return ''
  
  assign_array(dictionary, 3, c)
  w = c
  result.append(c)
  while True:
    if data['index'] > length:
      return ''
    bits = 0
    maxpower = pow(2, numBits)
    power = 1
    while power != maxpower:
      resb = data['val'] & data['position']
      data['position'] >>= 1
      if data['position'] == 0:
        data['position'] = resetValue
        data['val'] = getNextValue(data['index'])
        data['index'] += 1
      bits |= one_if_greater_than_zero(resb) * power
      power <<= 1
    
    c = bits
    old_c = c
    if old_c == 0:
      bits = 0
      maxpower = pow(2, 8)
      power = 1
      while power != maxpower:
        resb = data['val'] & data['position']
        data['position'] >>= 1
        if data['position'] == 0:
          data['position'] = resetValue
          data['val'] = getNextValue(data['index'])
          data['index'] += 1
        bits |= one_if_greater_than_zero(resb) * power
        power <<= 1
      assign_array(dictionary, dictSize, unichr(bits))
      dictSize += 1
      c = dictSize - 1
      enlargeIn -= 1
    elif old_c == 1:
      bits = 0
      maxpower = pow(2, 16)
      power = 1
      while power != maxpower:
        resb = data['val'] & data['position']
        data['position'] >>= 1
        if data['position'] == 0:
          data['position'] = resetValue
          data['val'] = getNextValue(data['index'])
          data['index'] += 1
        bits |= one_if_greater_than_zero(resb) * power
        power <<= 1
      assign_array(dictionary, dictSize, unichr(bits))
      dictSize += 1
      c = dictSize - 1
      enlargeIn -= 1
    elif old_c == 2:
      return ''.join(result)
    
    if enlargeIn == 0:
      enlargeIn = pow(2, numBits)
      numBits += 1
    
    if len(dictionary) > c and dictionary[c]:
      entry = dictionary[c]
    else:
      if c == dictSize:
        entry = w + w[0]
      else:
        return ''
    result.append(entry)
    
    assign_array(dictionary, dictSize, w + entry[0])
    dictSize += 1
    enlargeIn -= 1
    
    w = entry
    
    if enlargeIn == 0:
      enlargeIn = pow(2, numBits)
      numBits += 1