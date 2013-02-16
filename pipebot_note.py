# Pipebot notification plugin

from trac.core import *
from trac.wiki import IWikiChangeListener
from trac.ticket import ITicketChangeListener

import urllib

pipebot_file = "/tmp/hash-srobo"

class PipebotNotePlugin(Component):
	implements(IWikiChangeListener, ITicketChangeListener)

	# IWikiChangeListener API
	def wiki_page_added(self, page):
		self.write_message("A new wiki page %s has been created" % self.bold(page.name))

	def wiki_page_changed(self, page, version, t, comment, author, ipnr):
		self.write_message("Wiki page %s modified by %s (%s): %s" % (self.bold(page.name), self.green(author), comment, self.wiki_link(page)))

	def wiki_page_deleted(self, page):
		self.write_message("Wiki page %s deleted" % self.bold(page.name))

	def wiki_page_version_deleted(self, page):
		self.write_message("A version of wiki page %s has been deleted" % self.bold(page.name))
	
	def wiki_page_renamed(self, page, old_name):
		self.write_message("Wiki page %s renamed to %s" % (self.bold(old_name), self.bold(page.name)))
	
	# ITicketChangeListener
	def ticket_created(self, ticket):
		self.write_message("Ticket %s created by %s: %s" % (self.bold(ticket["summary"]), self.green(ticket["reporter"]), self.ticket_link(ticket)))
	
	def ticket_changed(self, ticket, comment, author, old_values):
		self.write_message("Ticket %s modified by %s: %s" % (self.bold(ticket["summary"]), self.green(author), self.ticket_link(ticket)))

	def ticket_deleted(self, ticket):
		self.write_message("Ticket %s deleted" % self.bold(ticket["summary"]))

	def write_message(self, msg):
		self.log.debug("Pipebot msg: \"%s\"" % msg)
		f = open(pipebot_file, 'a')
		f.write("%s: %s\n" % (self.orange("trac"), msg))
		f.close()

	def green(self, text):
		return "\x033%s\x0f" % text
	
	def orange(self, text):
		return "\x037%s\x0f" % text
	
	def bold(self, text):
		return "\x02%s\x02" % text

	def ticket_link(self, ticket):
		return "http://trac.srobo.org/ticket/%s" % ticket.id

	def wiki_link(self, page):
		return "http://trac.srobo.org/wiki/%s?action=diff&version=%i&old_version=%i" % (urllib.quote(page.name), page.version, page.version-1)
