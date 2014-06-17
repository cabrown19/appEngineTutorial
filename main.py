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

form = """
<form method="post">
What is your birthday?
    <br>
    <label> Month
        <input name="Month">
    </label>

    <label> Day
        <input name="Day">
    </label

    <label> Year
        <input name="Year">

    </label>
    <br>
    <br>
    <input type="submit">
</form>
"""

def escape_html(s):
    newString = ""
    for char in s:
        if char == '>':
            newString += "&gt;"
        elif char == '<':
            newString += "&lt;"
        elif char == '"':
            newString += "&quote;"
        elif char == '&':
            newString += "&amp;"
        else: 
            newString += char
    return newString


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(form)

    def post(self):
        self.response.write("Thanks! That's a totally valid day")

app = webapp2.WSGIApplication([
    ('/', MainHandler, )
], debug=True)
