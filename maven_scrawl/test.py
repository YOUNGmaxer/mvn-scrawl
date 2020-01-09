f = open('./assets/list.txt')
line = f.readline()
frame_list = []
while line:
  line = line.lower()
  frame_list.append(line)
  line = f.readline()
print(frame_list, len(frame_list))
f.close()