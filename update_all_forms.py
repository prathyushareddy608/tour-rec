#!/usr/bin/env python3
import os
import re

# List of all ticket files to update
ticket_files = [
    'Frontend/src/Agra/Ticket_Taj.js',
    'Frontend/src/Agra/Ticket_Fathepur.js',
    'Frontend/src/Agra/Ticket_Fort.js',
    'Frontend/src/Hyderabad/Ticket_Chowmahalla.js',
    'Frontend/src/Hyderabad/Ticket_Falaknuma.js',
    'Frontend/src/Hyderabad/Ticket_Golconda.js',
    'Frontend/src/Jaipur/Ticket_AmberPalace.js',
    'Frontend/src/Jaipur/Ticket_HawaMahal.js',
    'Frontend/src/Jaipur/Ticket_Jantarmantar.js',
    'Frontend/src/Kolkata/Ticket_IndianMuseum.js',
    'Frontend/src/Kolkata/Ticket_jorasanko.js',
    'Frontend/src/Kolkata/Ticket_VictorianMuseum.js',
    'Frontend/src/NewDelhi/Ticket_Humayun.js',
    'Frontend/src/NewDelhi/Ticket_QurubMinar.js',
    'Frontend/src/NewDelhi/Ticket_RedFort.js',
    'Frontend/src/Pune/Ticket_AgaKhan.js',
    'Frontend/src/Pune/Ticket_Kelkar.js',
    'Frontend/src/Pune/Ticket_ShaniwarWada.js'
]

def update_form_file(file_path):
    """Update a single form file to add Aadhar upload functionality"""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Check if file already has useState import
    if 'useState' not in content:
        # Add useState to imports
        content = content.replace(
            'import React, { useReducer} from "react";',
            'import React, { useReducer, useState} from "react";'
        )
    
    # Add file upload state and handler if not present
    if 'fileName' not in content:
        # Find the handleInput function and add file upload handlers after it
        handler_code = '''
  const handleFileUpload = (evt) => {
    const file = evt.target.files[0];
    if (file) {
      setFileName(file.name);
      setAadharFile(file);
    }
  };'''
        
        # Add state variables
        state_code = '''
 const [fileName, setFileName] = useState('');
 const [aadharFile, setAadharFile] = useState(null);
'''
        
        content = content.replace(
            'export function Ticket(props) {\n \n const handleInput',
            f'export function Ticket(props) {{\n{state_code}\n const handleInput'
        )
        
        content = content.replace(
            '  };',
            f'  }};{handler_code}',
            1  # Only replace the first occurrence
        )
    
    # Add encType to form if not present
    if 'encType="multipart/form-data"' not in content:
        content = content.replace(
            'action="/book/" method="post"',
            'action="/book/" method="post" encType="multipart/form-data"'
        )
    
    # Add senior citizen field if not present
    if 'count_senior' not in content:
        content = content.replace(
            '"count_abroad":"string",',
            '"count_abroad":"string",\n      "count_senior":"string",'
        )
    
    # Add senior citizen pricing
    if 'price_senior' not in content:
        content = content.replace(
            '<input type="hidden" name="price_abroad" value="1050"/>',
            '<input type="hidden" name="price_abroad" value="1050"/>\n          <input type="hidden" name="price_senior" value="23"/>'
        )
    
    # Add senior citizen dropdown if not present
    if 'Senior Citizens (60+)' not in content:
        senior_dropdown = '''  <Col>Senior Citizens (60+)<br></br>
  <Select
          labelId="demo-simple-select-label"
          name="count_senior"
          id="demo-simple-select"
          defaultValue={formInput.name}
          onChange={handleInput}
  >       
          <MenuItem value="0">0</MenuItem>
          <MenuItem value="1">1</MenuItem>
          <MenuItem value="2">2</MenuItem>
          <MenuItem value="3">3</MenuItem>
          <MenuItem value="4">4</MenuItem>
          <MenuItem value="5">5</MenuItem>
          <MenuItem value="6">6</MenuItem>
          <MenuItem value="7">7</MenuItem>
          <MenuItem value="8">8</MenuItem>
          <MenuItem value="9">9</MenuItem>
          <MenuItem value="10">10</MenuItem>
  </Select></Col>'''
        
        # Insert after foreigners dropdown
        content = content.replace(
            '  </Select></Col>\n  \n  \n   \n    \n  </Row>',
            f'  </Select></Col>\n{senior_dropdown}\n  \n  \n   \n    \n  </Row>'
        )
    
    # Update pricing table
    if 'Children below 12 years' not in content:
        content = content.replace(
            'Children below 15 years',
            'Children below 12 years'
        )
    
    # Add Aadhar upload field before the submit button if not present
    if 'Upload Aadhar Card' not in content:
        upload_field = '''
  <Row>
    <Col>
      <Form.Group className="mb-3">
        <Form.Label>Upload Aadhar Card (PDF/Image)</Form.Label>
        <Form.Control 
          type="file" 
          name="aadharCard" 
          accept=".pdf,image/*" 
          onChange={handleFileUpload}
        />
        {fileName && <small className="text-muted">Selected file: {fileName}</small>}
      </Form.Group>
    </Col>
  </Row>
  '''
        
        # Insert before submit button
        content = content.replace(
            '  <Button type="submit">Book Now</Button>',
            f'{upload_field}\n  <Button type="submit">Book Now</Button>'
        )
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"Updated: {file_path}")

# Update all files
for file_path in ticket_files:
    update_form_file(file_path)

print("All booking forms updated successfully!")
