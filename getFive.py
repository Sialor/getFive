from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import string
import random
import time

# questions table
questions = {}

#try
test = {}

def next_string(string):
	if string == '1' * len(string):
		print('next string not create because string is ' + string)
		exit(1)
	
	string = string[:-1] + str(int(string[-1]) + 1)[0]
	
	while True:
		for i in range(len(string) - 1, -1, -1):
			if string[i] == '2':
				string = string[0:i] + '0' + string[i + 1:]
				string = string[0:i - 1] + str(int(string[i - 1]) + 1) + string[i - 1 + 1:]
				break

		if string.rfind('2') == -1:
			break

	return string

def next_string_digit(string):
	if string.count('1') == 0:
		string = string[:-1] + '1'
		return string
	elif string.count('1') > 1 or string[0] == '1':
		print('next string not create because string is ' + string)
		exit(1)
	
	idx = string.index('1')
	return '0' * (idx - 1) + '1' + '0' * (len(string) - idx)

def write_struct():
	file = open('structs', 'w')
	#file.write(str(questions.items()) + '\n')
	
	for i in questions.keys():
		file.write(str(i) + ' ' + questions.get(i) + '\n')

	file.write('\n')

	for i in test.keys():
		item = test.get(i)
		string = str(i) + ':\n' + str(len(item) - 2) + '\n'
		string += '\n'.join(list(map(lambda x: str(x), item)))
		string += '\n'
		file.write(string)
	
	file.close()

def read_struct():
	try:
		file = open('structs', 'r')
	except FileNotFoundError:
		return

	# чтение словаря "idx: question"
	idx = file.readline()
	while len(idx) > 1:
		questions.update({int(idx[:idx.index(' ')]): idx[idx.index(' ') + 1:-1]})
		idx = file.readline()

	# чтение словаря "idx: [answers, ..., '101', 'y']"
	answers = []
	idx = file.readline()
	while ':' in idx:
		idx = idx[:-2]
		for i in range(int(file.readline()) + 2):
			answers += [file.readline().replace('\n', '')]
		
		test.update({int(idx):answers})
		answers = []
		idx = file.readline()
	
	file.close()

def save_correct_answers():
	file_answers = open('answers.txt', 'w')
	
	for i in test.keys():
		if test.get(i)[-1] == 'y':
			file_answers.write(questions.get(i) + '\n\tОтветы:\n')
			string = test.get(i)[-2][::-1]
			for j in (k for k in range(len(string)) if string[k] == '1'):
				file_answers.write('\t' + test.get(i)[j] + '\n')

	file_answers.close()

def random_string():
	return random.choice(string.ascii_letters) +\
	random.choice(string.ascii_letters) +\
	random.choice(string.ascii_letters)

def find_element_by_text(driver, tag, text):
	for i in driver.find_elements_by_tag_name(tag):
		if i.text == text:
			return i

def get_name_test(n_test):
	if n_test == 0:
		return find_element_by_text(browser, 'a', 'Введение в веб')
	elif n_test == 1:
		return find_element_by_text(browser, 'a', 'Верстка и основы html')
	elif n_test == 2:
		return find_element_by_text(browser, 'a', 'Основы CSS')
	elif n_test == 3:
		return find_element_by_text(browser, 'a', 'Основы javascript')
	else:
		return find_element_by_text(browser, 'a', 'Основы Vue.js')

def get_half_size_test(n_test):
	return 6 if not n_test else 14

debug = open('info.txt', 'a+')

# Register to iti.i-aos.ru
browser = webdriver.Firefox()
browser.get('http://iti.i-aos.ru/register')

read_struct()

browser.execute_script("window.scrollTo(0, 80);")

debug.write(time.asctime() + '\n')
debug.write('we in register\n')

password = random_string() * 3

element = browser.find_element_by_id('first_name')
element.send_keys(random_string())
element = browser.find_element_by_id('name')
element.send_keys(random_string())
element = browser.find_element_by_id('second_name')
element.send_keys(random_string())
element = browser.find_element_by_id('password')
element.send_keys(password)
element = browser.find_element_by_id('password-confirm')
element.send_keys(password)
element = browser.find_element_by_id('email')
element.send_keys(random_string() + '@mail.ru')
element = browser.find_element_by_css_selector('div.select-wrapper')
element.find_element_by_tag_name('input').click()
element.find_element_by_tag_name('ul').find_elements_by_tag_name('li')[1].click()

debug.write('we fill all inputs\n')

element = browser.find_element_by_tag_name('form').submit()

debug.write('we finish register\n')

max_iteration = 100
iterations = 0

n_test = 4

current_question = ''
current_answers = []
current_help = ''
current_number_question = 0

time.sleep(5)
element = find_element_by_text(browser, 'i', 'arrow_drop_down').click()
time.sleep(0.5)
element = find_element_by_text(browser, 'a', 'Программирование веб-интерфейсов').click()
time.sleep(3.6)
element = find_element_by_text(browser, 'i', 'view_headline').click()
time.sleep(3.6)

element = get_name_test(n_test)

element.click()

time.sleep(3.6)
element = find_element_by_text(browser, 'a', 'Пройти тестирование по теме').click()

debug.write('fecit prepare\n')
debug.write('start bruteforse\n')

while True:
	time.sleep(0.5)
	find_element_by_text(browser, 'a', 'НАЧАТЬ ТЕСТ').click()

	for qu in range(get_half_size_test(n_test)):
		time.sleep(0.05)
		tmp_flag = False
		current_help = browser.find_element_by_id('help').find_element_by_tag_name('i').text
		current_question = browser.find_element_by_id('question').find_element_by_tag_name('p').text
		current_question_idx = int(browser.find_element_by_id('question_id').get_attribute('value'))
		current_answers = browser.find_elements_by_class_name('answer-item')
		current_number_question = int(browser.find_element_by_id('number').find_element_by_tag_name('span').text)
	
		tmp_flag = current_question_idx in questions.keys()

		if not tmp_flag:
			test.update({current_question_idx:list(map(lambda webelement: webelement.find_element_by_tag_name('span').text, current_answers)) + ['0' * (len(current_answers) - 1) + '1', 'n']})
			questions.update({current_question_idx: current_question})
		elif test.get(current_question_idx)[-1] == 'n':
			tmp_flag = False

		# Select answer
		time.sleep(0.25)
		if not tmp_flag:
			string = test.get(current_question_idx)[-2][::-1]
			for j in (test.get(current_question_idx)[i] for i in range(len(string)) if string[i] == '1'):
				find_element_by_text(browser, 'span', j).click()

			break
		elif qu < get_half_size_test(n_test) - 1:
			find_element_by_text(browser, 'i', 'chevron_right').click()

	# Skip test
	time.sleep(0.35)
	find_element_by_text(browser, 'a', str(current_number_question)).click()
	time.sleep(0.5)
	#Message: The element reference of <i> is stale; either the element is no longer attached to the DOM, it is not in the current frame context, or the document has been refreshed
	find_element_by_text(browser, 'i', 'chevron_right').click()
	time.sleep(0.35)
	browser.find_element_by_id('finish-test').click()

	time.sleep(0.6)

	# Check success
	element = browser.find_elements_by_class_name('line')[1]
	success = element.text[-1] == '1'

	# Write answer
	if success:
		test.get(current_question_idx)[-1] = 'y'
	elif not tmp_flag:
		string = test.get(current_question_idx)[-2]
		string = next_string(string) if current_help == 'Выберите несколько правильных вариантов' else next_string_digit(string)
		test.get(current_question_idx)[-2] = string

	write_struct()
	if iterations % 2 == 1:
		save_correct_answers()

	iterations += 1

	if iterations >= max_iteration:
		break

	# Repeat test
	find_element_by_text(browser, 'a', 'ПРОЙТИ ТЕСТИРОВАНИЕ ЕЩЕ РАЗ').click()

debug.close()
write_struct()
save_correct_answers()
browser.quit()