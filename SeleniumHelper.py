from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class SeleniumHelper:
	driver = None
	WAIT = 99999

	def loadPage(self, page):
		try:
			self.driver.get(page)
			return True
		except:
			return False

	def submitForm(self, element):
		try:
			element.submit()
			return True
		except TimeoutException:
			return False

	def waitShowElement(self, selector, wait=99999):
		try:
			wait = WebDriverWait(self.driver, wait)
			element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
			return element
		except:
			return None

	def waitHideElement(self, selector, wait):
		try:
			wait = WebDriverWait(self.driver, wait)
			element = wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, selector)))
			return element
		except:
			return None

	def getElementFrom(self, fromObject, selector):
		try:
			return fromObject.find_element_by_css_selector(selector)
		except NoSuchElementException:
			return None

	def getElementsFrom(self, fromObject, selector):
		try:
			return fromObject.find_elements_by_css_selector(selector)
		except NoSuchElementException:
			return None		

	def getElement(self, selector):
		return self.getElementFrom(self.driver, selector)

	def getElements(self, selector):
		return self.getElementsFrom(self.driver, selector)

	def getElementFromValue(self, fromObject, selector):
		element = self.getElementFrom(fromObject, selector)
		return self.getValue(element)

	def getElementValue(self, selector):
		element = self.getElement(selector)
		return self.getValue(element)

	def getValue(self, element):
		if element:
			return element.text
		return None

	def getAttribute(self, element, attribute):
		if element:
			return element.get_attribute(attribute)
		return None

	def getElementFromAttribute(self, fromObject, selector, attribute):
		element = self.getElementFrom(fromObject, selector)
		return self.getAttribute(element, attribute)

	def getElementAttribute(self, selector, attribute):
		element = self.getElement(selector)
		return self.getAttribute(element, attribute)

	def getParentLevels(self, node, levels):
		path = '..'
		if levels > 1:
			for i in range(1, levels):
				path = path + '/..'
		return node.find_element_by_xpath(path)

	def getParentNode(self, node):
		return node.find_element_by_xpath('..')

	def getChildNodes(self, node):
		return node.find_elements_by_xpath('./*')

	def selectAndWrite(self, field, value):
		fieldObject = self.getElement(field)
		fieldObject.send_keys(value)
		return fieldObject

	def waitAndWrite(self, field, value):
		fieldObject = self.waitShowElement(field, self.WAIT)
		fieldObject.send_keys(value)
		return fieldObject

	def pressEnter(self, fieldObject):
		fieldObject.send_keys(Keys.RETURN)
		return fieldObject

	def clickSelector(self, selector):
		element = self.getElement(selector)
		if element:
			try:
				actions = webdriver.ActionChains(self.driver)
				actions.move_to_element(element)
				actions.click(element)
				actions.perform()
				return True
			except:
				return False
		return False

	def click(self, element):
		actions = webdriver.ActionChains(self.driver)
		actions.move_to_element(element)
		actions.click(element)
		actions.perform()

	def moveToElement(self, element):
		self.driver.execute_script("return arguments[0].scrollIntoView();", element)
		actions = webdriver.ActionChains(self.driver)
		actions.move_to_element(element)
		actions.perform()

	def scrollDown(self):
		self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	def scrollingDown(self, times):
		for i in range(1, times):
			self.scrollDown()
			time.sleep(0.5)

	def getFieldValue(self, record, parent=None):
		exit = None
		if parent:
			if record['type'] == 'attr':
				if record['selector']:
					exit = self.getElementFromAttribute(parent, record['selector'], record['attr'])
				else:
					exit = self.getAttribute(parent)
			elif record['type'] == 'text':
				if record['selector']:
					exit = self.getElementFromValue(parent, record['selector'])
				else:
					exit = self.getValue(parent)
			elif record['type'] == 'style':
				exit = record['attr']
		else:
			if record['type'] == 'attr':
				exit = self.getElementAttribute(record['selector'], record['attr'])
			elif record['type'] == 'text':
				exit = self.getElementValue(record['selector'])
			elif record['type'] == 'style':
				exit = record['attr']
		return exit

	def extractSection(self, section):
		exit = {}
		for subsection in self.SECTIONS[section]:
			container = self.SECTIONS[section][subsection]
			if container['quantity'] == 'multiple':
				exit[subsection] = []
				elements = self.getElements(container['selector'])
				for element in elements:
					row = {}
					for field in self.FIELDS[section][subsection]:
						record = self.FIELDS[section][subsection][field]
						row[field] = self.getFieldValue(record, element)
					exit[subsection].append(row)
			elif container['quantity'] == 'single':
				exit[subsection] = self.getFieldValue(container)
		return exit

	def saveScreenshoot(self, filePath):
		self.driver.save_screenshot(filePath)

	def loadAndWait(self, url, selector, wait=9999):
		self.loadPage(url)
		return self.waitShowElement(selector, wait)

	def close(self):
		self.driver.quit()