#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re
import os
import jinja2

####################################################################################
form = """
<h2> Enter some text to ROT%(ROT)s <h2>
<form method="post">
    <textarea name="text" style="height: 100px; width: 400px;">%(TEXT)s</textarea>
    <br>
    <input type="submit">
</form>
"""
####################################################################################
ROTform = """
<h2> What ROT value would you like? <h2>
<form method="post">
    <input type="text" name="ROT">
    <br>
    <input type="submit">
</form>
"""
####################################################################################
signupForm = """
<html><head>
    <title>Sign Up</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>

  </head>

  <body>
    <h2>Signup</h2>
    <form method="post">
      <table>
        <tbody><tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(USER)s">
          </td>
          <td class="error">
            %(UNERROR)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="">
          </td>
          <td class="error">
            %(PASSERROR)s
            
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="">
          </td>
          <td class="error">
            %(MATCHERROR)s
            
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(EMAIL)s">
          </td>
          <td class="error">
            %(EMAILERROR)s
            
          </td>
        </tr>
      </tbody></table>

      <input type="submit">
    </form>
</body></html>
"""

####################################################################################
def escape_html(s):
    return cgi.escape(s, quote = True)

####################################################################################
def cypher(s, rotVal):
    newString = ""
    for char in s:
        val = ord(char)
        if val > 64 and val < 91:
            val = val + rotVal
            if val > 90:
                val = val - 26
        elif val > 96 and val < 123:
            val = val + rotVal
            if val > 122:
                val = val - 26
        newString += chr(val)
    return newString

####################################################################################
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

####################################################################################
PASS_RE = re.compile(r"^.{3,20}$")
def valid_pass(password):
    return PASS_RE.match(password)

####################################################################################
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)

####################################################################################
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("<h2>Welcome to my AppEngine tutorial!</h2>")

####################################################################################
class ROTnumHandler(webapp2.RequestHandler):
    def write_form(self):
        self.response.write(ROTform)

    def get(self):
        self.write_form()

    def post(self):
        rotVal = escape_html(self.request.get('ROT'))
        self.redirect('/hw2p1/rot?ROT=%s'%rotVal)

####################################################################################
class ROThandler(webapp2.RequestHandler):
    def write_form(self, user_text = ""):
        rotVal = self.request.get("ROT")
        self.response.write(form %{"ROT": str(rotVal), "TEXT": user_text})

    def get(self):
        self.write_form()

    def post(self):
        rotVal = self.request.get("ROT")
        user_text = escape_html(cypher(self.request.get('text'), int(rotVal)))
        self.write_form(user_text)

####################################################################################
class signupHandler(webapp2.RequestHandler):
    def write_form(self, username = "", email = "", UNe = "", p1e = "", p2e = "", ee = ""):
        self.response.write(signupForm%{"USER": username, "UNERROR": UNe, "PASSERROR": p1e, "MATCHERROR": p2e, "EMAIL": email, "EMAILERROR": ee})

    def get(self):
        self.write_form()

    def post(self):
        user_name = self.request.get('username')
        user_pass1 = self.request.get('password')
        user_pass2 = self.request.get('verify')
        user_email = self.request.get('email')

        valid_name = (valid_username(user_name) != None)
        valid_pass1 = (valid_pass(user_pass1) != None)
        valid_pass2 = (user_pass2 == user_pass1) and valid_pass1
        valid_em = (valid_email(user_email) != None) or (user_email == "")

        if (not valid_name):
            UNe = "Invalid Username"
        else:
            UNe = ""
        
        if (not valid_pass1):
            p1e = "Passord must be between 3 and 20 characters"
        else: 
            p1e = ""

        if (not valid_pass2):
            p2e = "Passords don't match!"
        else: 
            p2e = ""

        if (not valid_em):
            ee = "Invalid Email"
        else: 
            ee = ""

        if (valid_name and valid_pass1 and valid_pass2 and valid_em):
            self.redirect("/hw2p2/welcome?username=%s"%user_name)

        else:
            self.write_form(user_name, user_email, UNe, p1e, p2e, ee) 

        return

####################################################################################
class welcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.write("<h2> Welcome %s</h2>"%username)

####################################################################################
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape)

####################################################################################
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

####################################################################################
class l2aHandler(Handler):
    def get(self):
        items = self.request.get_all("food")
        self.render("shopping_list.html", items = items)

####################################################################################
app = webapp2.WSGIApplication([
    ('/', MainHandler, ),
    ('/hw2p1', ROTnumHandler),
    ('/hw2p1/rot', ROThandler),
    ('/hw2p2', signupHandler),
    ('/hw2p2/welcome', welcomeHandler),
    ('/lesson2a', l2aHandler)
], debug=True)
