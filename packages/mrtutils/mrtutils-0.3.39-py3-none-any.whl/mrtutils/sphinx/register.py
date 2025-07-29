"""
Sphinx directive for creating register layout tables.

This directive creates visual register layout tables showing bit fields,
values, and descriptions in a clear tabular format.

Usage:


    .. register::
        :bitwidth: 32
        :width: 400
        :show-bits:
        :show-field-descriptions:

        UART_CONFIG_0: 
            Baud: { bits: 31-8, description: Baud rate for the UART interface }
            DataBits: { bits: 7-3, description: Number of data bits in the UART frame }
            StopBits: 
                bits: 3-2
                description: Number of stop bits used in the UART communication
                values:
                    1BIT: 1
                    1_5BIT: 2
                    2bit: 3
            Parity: 
                bits: 1-0
                values:
                    NONE: 0
                    ODD: 1
                    EVEN: 2

        UART_CONFIG_1: 
            IDLE_BITS: { bits: 31-24, description: Number of idle to wait before sending received data}
            TX: { bits: 15-8, description: 'Id for TX signal. 0x00 for RX only' }
            RX: { bits: 7-0, description: 'Id for RX signal. 0x00 for TX only' }

    .. register:: path/to/registers.yml
        :bitwidth: 32
        :width: 400
        :show-bits:
        :show-field-descriptions:

        #only show specific registers from the file
        UART_CONFIG_0
        UART_CONFIG_1

Notes: 

    bits can be degined as a range ('31-25', '31:25) a single bit ('31', '25') or a size (':4') 


"""

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.statemachine import ViewList
import yaml
import re
from mrtutils.device import DeviceSpec

class RegisterDirective(Directive):
    """
    Directive to create register layout tables.
    
    Options:
        - bitwidth: Total bit width (default: 32)
        - width: Table width in pixels (default: 600)
        - show-bits: Show individual bit numbers in headers
        - layout: 'visual' or 'table' (default: visual)
        - rowwidth: Bits per row for wrapping (default: 32)
        - show-field-descriptions: Show descriptions table
        - desc-table-width: Width of descriptions table in pixels
        - desc-field-width: Field column width percentage (0-100)
    """

    optional_arguments = 1
    required_arguments = 0
    has_content = True
    option_spec = {
        'bitwidth': directives.positive_int,
        'width': directives.positive_int,
        'show-bits': directives.flag,
        'layout': directives.unchanged,  # 'visual' or 'table' (default: visual)
        'rowwidth': directives.positive_int,  # Bits per row for wrapping (default: 32)
        'show-field-descriptions': directives.flag,  # Show descriptions table
        'desc-table-width': directives.positive_int,  # Width of descriptions table in pixels
        'desc-field-width': directives.positive_int,  # Field column width percentage (0-100)
    }
    
    def run(self):
        # Get options with defaults
        bitwidth = self.options.get('bitwidth', 32)
        table_width = self.options.get('width', 600)
        show_bits = 'show-bits' in self.options
        layout = self.options.get('layout', 'visual')
        rowwidth = self.options.get('rowwidth', bitwidth)
        show_field_descriptions = 'show-field-descriptions' in self.options

        # Parse the content as YAML
        filePath = self.arguments[0] if self.arguments else None 

        device = None 
        filter = None


        if filePath:
            # Load YAML from file
            device = DeviceSpec() 
            device.parseYAML(filePath)

            if len(self.content) > 0:
                filter = [line.strip() for line in self.content if line.strip()]
        
        else: 

            content_str = '\n'.join(self.content)
            try:
                # Convert the content to proper YAML
                yaml_content = self._convert_to_yaml(content_str)
                parsed_data = yaml.safe_load(yaml_content)

                dummy_wrapper = {
                    'registers': [],
                    'fields': parsed_data
                }

                device = DeviceSpec()
                device.parseYAML(dummy_wrapper)


            except yaml.YAMLError as e:
                error = self.state_machine.reporter.error(
                    f'Error parsing register fields: {e}',
                    nodes.literal_block(self.block_text, self.block_text),
                    line=self.lineno
                )
                return [error]
            
        result = []
        allFields = []

        for name, reg in device.regs.items():

            if filter is None or name in filter:
                for field in reg.fields:
                    allFields.append(field)
        
        for name, reg in device.regs.items():

            if filter is None or name in filter:
                if layout == 'table':
                    result.extend(self._create_register_table(name, reg.fields, reg.size * 8 , table_width))
                else:
                    result.extend(self._create_visual_layout(name, reg.fields, reg.size * 8, show_bits, rowwidth, table_width))

                if len(device.regs.keys()) > 1:
                    spacing = nodes.paragraph()
                    spacing.attributes['style'] = 'margin-top: 2em 0;'
                    result.append(spacing)
        

        if show_field_descriptions:
            desc_table_width = self.options.get('desc-table-width', None)
            desc_field_width = self.options.get('desc-field-width', 20)
            desc_table = self._create_descriptions_table(allFields, desc_table_width, desc_field_width)
            if desc_table:
                result.extend(desc_table)
        
        return result

        



    def _convert_to_yaml(self, content):
        """Convert the RST content to proper YAML"""
        lines = content.strip().split('\n')
        yaml_lines = []
        
        for line in lines:
            # Remove inline comments but preserve the line structure
            if '#' in line:
                line = line.split('#')[0].rstrip()
            
            # Skip empty lines and pure comment lines
            if not line.strip():
                continue
            
            # Handle different line types
            if ':' in line and not line.strip().startswith('-'):
                # This could be a key-value line
                yaml_lines.append(line)
            elif line.startswith('- {') and line.endswith('}'):
                # Legacy list format - still supported
                yaml_lines.append(line)
            elif line.startswith('-'):
                # Other list formats
                yaml_lines.append(line)
            else:
                # Continuation lines (indented content)
                yaml_lines.append(line)

        
        return '\n'.join(yaml_lines)
    
    def _create_register_table(self, title, fields, bitwidth, table_width):
        """Create a traditional register layout table (original format)"""
        
        # Create container
        container = nodes.container()
        
        # Add title
        if title:
            title_para = nodes.paragraph()
            title_strong = nodes.strong(text=title)
            title_para += title_strong
            container.append(title_para)
        
        # Create table
        table = nodes.table()
        
        #set width if specified
        if table_width:
            table.attributes['style'] = f'width: {table_width}px;'

        tgroup = nodes.tgroup(cols=4)
        table += tgroup
        
        # Define column widths (proportional)
        tgroup += nodes.colspec(colwidth=15)  # Bits
        tgroup += nodes.colspec(colwidth=20)  # Value  
        tgroup += nodes.colspec(colwidth=10)  # Width
        tgroup += nodes.colspec(colwidth=55)  # Description
        
        # Create header
        thead = nodes.thead()
        tgroup += thead
        
        header_row = nodes.row()
        thead += header_row
        
        headers = ['Bits', 'Value', 'Width', 'Name']
        for header in headers:
            entry = nodes.entry()
            entry += nodes.paragraph(text=header)
            header_row += entry
        
        # Create body
        tbody = nodes.tbody()
        tgroup += tbody
        
        # Sort fields by bit position (highest first)
        sorted_fields = sorted(fields, key=lambda f: f.highBit, reverse=True)
        
        # Add rows for each field
        for field in sorted_fields:
            row = nodes.row()
            tbody += row
            
            # Bits column
            bits_entry = nodes.entry()
            bits_entry += nodes.paragraph(text=field.bit_range)
            row += bits_entry
            
            # Value column
            value_entry = nodes.entry()
            # Use literal for hex values and code-like content
            if field.value and (field.value.startswith('0x') or field.value.startswith('<')):
                value_entry += nodes.literal(text=field.value)
            else:
                value_entry += nodes.paragraph(text=field.value)
            row += value_entry
            
            # Width column
            width_entry = nodes.entry()
            width_entry += nodes.paragraph(text=str(field.width))
            row += width_entry
            
            # Name column
            name_entry = nodes.entry()
            name_entry += nodes.paragraph(text=field.name)
            row += name_entry
        
        container += table
        return [container]
    
    def _create_visual_layout(self, title, fields, total_packet_width, show_bits, rowwidth, table_width):
        """Create a visual packet layout table similar to protocol diagrams"""
        
        # Create container
        container = nodes.container()
        
        # Add title
        if title:
            title_para = nodes.paragraph()
            title_strong = nodes.strong(text=title)
            title_para += title_strong
            container.append(title_para)
        
        # Sort fields by bit position (highest first)
        sorted_fields = sorted(fields, key=lambda f: f.highBit, reverse=True)
        
        # Calculate how many rows we need based on total packet width and rowwidth
        num_rows = (total_packet_width + rowwidth - 1) // rowwidth  # Ceiling division
        
        # Create table
        table = nodes.table()
        table['classes'] = ['packet-layout']
        if table_width:
            table['classes'].append(f"width-{table_width}")
        tgroup = nodes.tgroup(cols=rowwidth)
        table += tgroup
        
        # Define column widths - all bit columns equal width
        for i in range(rowwidth):
            tgroup += nodes.colspec(colwidth=3)  # Individual bit columns
        
        # Create thead and tbody
        thead = nodes.thead()
        tgroup += thead
        tbody = nodes.tbody()
        tgroup += tbody
        
        # Create single header row when show_bits is enabled
        if show_bits:
            header_row = nodes.row()
            header_row['classes'] = ['packet-header-row']
            thead += header_row
            
            # Show bit numbers from rowwidth-1 down to 0
            for bit_pos in range(rowwidth):
                bit_number = rowwidth - 1 - bit_pos
                bit_cell = nodes.entry()
                bit_cell['classes'] = ['packet-bit-header']
                # Use strong for bit numbers to make them stand out
                bit_para = nodes.paragraph()
                bit_strong = nodes.strong(text=str(bit_number))
                bit_para += bit_strong
                bit_cell += bit_para
                header_row += bit_cell
        
        # Process each row
        for row_num in range(num_rows):
            # Calculate bit range for this row
            row_highBit = total_packet_width - 1 - (row_num * rowwidth)
            row_lowBit = max(0, row_highBit - rowwidth + 1)
            
            # Create header row for this section (only when not showing bits)
            if not show_bits:
                header_row = nodes.row()
                header_row['classes'] = ['packet-header-row']
                
                # Add to thead for first row, tbody for subsequent rows
                if row_num == 0:
                    thead += header_row
                else:
                    tbody += header_row
                
                # Show field ranges that fall in this row
                self._add_range_header_row(header_row, sorted_fields, row_highBit, row_lowBit, rowwidth)
            
            # Create data row for this section
            data_row = nodes.row()
            data_row['classes'] = ['packet-data-row']
            tbody += data_row
            
            # Add field data for this row
            self._add_data_row(data_row, sorted_fields, row_highBit, row_lowBit, rowwidth)
        
        container += table
        return [container]
    
    def _add_range_header_row(self, header_row, sorted_fields, row_highBit, row_lowBit, rowwidth):
        """Add field range headers for the current row"""
        bit_pos = row_highBit
        
        while bit_pos >= row_lowBit:
            # Find field that contains this bit position
            field_found = False
            for field in sorted_fields:
                if field.lowBit <= bit_pos <= field.highBit:
                    # This field spans some bits in this row
                    # Calculate how many bits of this field are in this row
                    field_start_in_row = min(bit_pos, field.highBit)
                    field_end_in_row = max(row_lowBit, field.lowBit)
                    field_width_in_row = field_start_in_row - field_end_in_row + 1
                    
                    # Create spanning cell
                    field_cell = nodes.entry()
                    field_cell['classes'] = ['register-field-header']
                    if field_width_in_row > 1:
                        field_cell['morecols'] = field_width_in_row - 1
                    
                    # Show the appropriate range for this row
                    if field.highBit > row_highBit or field.lowBit < row_lowBit:
                        # Field spans multiple rows, show partial range
                        display_range = f"{field_start_in_row}:{field_end_in_row}"
                    else:
                        # Field is entirely in this row, show full range
                        display_range = field.bit_range
                    
                    # Use strong for field ranges to make them stand out
                    range_para = nodes.paragraph()
                    range_strong = nodes.strong(text=display_range)
                    range_para += range_strong
                    field_cell += range_para
                    header_row += field_cell
                    
                    bit_pos = field_end_in_row - 1
                    field_found = True
                    break
            
            if not field_found:
                # No field covers this bit, add empty cell
                empty_cell = nodes.entry()
                empty_cell['classes'] = ['register-empty-header']
                empty_cell += nodes.paragraph(text="")
                header_row += empty_cell
                bit_pos -= 1
    
    def _add_data_row(self, data_row, sorted_fields, row_highBit, row_lowBit, rowwidth):
        """Add field data for the current row"""
        bit_pos = row_highBit
        
        while bit_pos >= row_lowBit:
            # Find field that contains this bit position
            field_found = False
            for field in sorted_fields:
                if field.lowBit <= bit_pos <= field.highBit:
                    # This field spans some bits in this row
                    field_start_in_row = min(bit_pos, field.highBit)
                    field_end_in_row = max(row_lowBit, field.lowBit)
                    field_width_in_row = field_start_in_row - field_end_in_row + 1
                    
                    # Create spanning cell
                    data_cell = nodes.entry()
                    cell_classes = ['register-field-data']
                    
                    # Apply background color if specified
                    if field.color:
                        # Create a CSS-safe class name from the color
                        color_class = f'register-color-{self._color_to_class(field.color)}'
                        cell_classes.append(color_class)
                        # Store the actual color value in a data attribute
                        data_cell.attributes['data-register-color'] = field.color
                    
                    data_cell['classes'] = cell_classes
                    if field_width_in_row > 1:
                        data_cell['morecols'] = field_width_in_row - 1
                    
                    # Only show value/name if this is the main part of the field
                    # (i.e., the highest bit of the field is in this row)
                    if field.highBit <= row_highBit:
                        # If value is provided, show it in bold above the name
                        if field.value:
                            value_para = nodes.paragraph()
                            value_para['classes'] = ['register-field-value']
                            value_strong = nodes.strong(text=field.value)
                            value_para += value_strong
                            data_cell += value_para
                            
                            # Always show the name under the value, slightly muted
                            if field.name:
                                name_para = nodes.paragraph(text=field.name)
                                name_para['classes'] = ['register-field-name']
                                data_cell += name_para
                        else:
                            # Only name (no value)
                            if field.name:
                                name_para = nodes.paragraph(text=field.name)
                                name_para['classes'] = ['register-field-name-only']
                                data_cell += name_para
                    else:
                        # This is a continuation of a field from a previous row
                        # Show continuation indicator or leave empty
                        
                        cont_para = nodes.paragraph(text=f"{field.name} cont.. ")
                        cont_para['classes'] = ['register-field-continuation']
                        data_cell += cont_para
                    
                    data_row += data_cell
                    bit_pos = field_end_in_row - 1
                    field_found = True
                    break
            
            if not field_found:
                # No field covers this bit, add empty cell
                empty_cell = nodes.entry()
                empty_cell['classes'] = ['register-empty-data']
                empty_cell += nodes.paragraph(text="")
                data_row += empty_cell
                bit_pos -= 1
    
    def _color_to_class(self, color):
        """Convert a color value to a CSS-safe class name suffix"""
        import re
        # Remove special characters and convert to lowercase
        color_class = re.sub(r'[^a-zA-Z0-9]', '-', str(color).lower())
        # Remove multiple consecutive dashes
        color_class = re.sub(r'-+', '-', color_class)
        # Remove leading/trailing dashes
        color_class = color_class.strip('-')
        return color_class
    
    def _create_descriptions_table(self, fields, table_width=None, field_col_width=20, register_name=None):
        """Create a field descriptions table"""
        
        # Filter fields that have descriptions or values
        fields_with_descriptions = [
            field for field in fields 
            if field.desc != ''
        ]
        
        if not fields_with_descriptions:
            return []
        
        # Create container
        container = nodes.container()
        
        # Add spacing
        spacing = nodes.paragraph()
        container.append(spacing)
        
        # Add register-specific title for descriptions if we have multiple registers
        if register_name:
            desc_title = nodes.paragraph()
            desc_title_strong = nodes.strong(text=f"{register_name} Field Descriptions")
            desc_title += desc_title_strong
            container.append(desc_title)
        
        # Create table
        table = nodes.table()
        table['classes'] = ['register-descriptions']
        
        # Set table width if specified
        if table_width:
            table.attributes['style'] = f'width: {table_width}px;'
        
        tgroup = nodes.tgroup(cols=2)
        table += tgroup
        
        # Define column widths - use the provided field column width
        desc_col_width = 100 - field_col_width
        tgroup += nodes.colspec(colwidth=field_col_width)  # Field name column
        tgroup += nodes.colspec(colwidth=desc_col_width)   # Description column
        
        # Create header
        thead = nodes.thead()
        tgroup += thead
        
        header_row = nodes.row()
        thead += header_row
        
        # Field header
        field_header = nodes.entry()
        field_header['classes'] = ['register-desc-header']
        field_para = nodes.paragraph()
        field_strong = nodes.strong(text="Field")
        field_para += field_strong
        field_header += field_para
        header_row += field_header
        
        # Description header
        desc_header = nodes.entry()
        desc_header['classes'] = ['register-desc-header']
        desc_para = nodes.paragraph()
        desc_strong = nodes.strong(text="Description")
        desc_para += desc_strong
        desc_header += desc_para
        header_row += desc_header
        
        # Create body
        tbody = nodes.tbody()
        tgroup += tbody
        
        # Sort fields by bit position (highest first)
        #sorted_fields = sorted(fields_with_descriptions, key=lambda f: f.highBit, reverse=True)
        
        # Add rows for each field with description
        for field in fields_with_descriptions:
            row = nodes.row()
            tbody += row
            
            # Field name column
            name_entry = nodes.entry()
            name_entry['classes'] = ['register-desc-field-name']
            name_para = nodes.paragraph()
            name_strong = nodes.strong(text=field.name)
            name_para += name_strong
            name_entry += name_para
            row += name_entry
            
            # Description column
            desc_entry = nodes.entry()
            desc_entry['classes'] = ['register-desc-field-desc']
            
            # Add description if present
            if field.desc:
                desc_para = nodes.paragraph(text=field.desc)
                desc_entry += desc_para
            
            # Add values if present
            if field.vals:
                if field.desc:
                    # Add spacing between description and values
                    spacing_para = nodes.paragraph()
                    desc_entry += spacing_para
                
                # Add "Values:" label
                values_label = nodes.paragraph()
                values_strong = nodes.strong(text="Values:")
                values_label += values_strong
                desc_entry += values_label
                
                # Add each value
                for fieldVal in field.vals:
                    value_para = nodes.paragraph()
                    

                    value_code = fieldVal.val 
                    value_desc = fieldVal.desc
                    
                    # Format: "    0x00: OK" or "    0x00: OK - Description"
                    value_text = f"        {value_code}: {fieldVal.name}"
                    if value_desc:
                        value_text += f" - {value_desc}"
                    
                    value_para += nodes.Text(value_text)
                    desc_entry += value_para
            
            row += desc_entry
        
        container += table
        return [container]
    
def setup(app):
    """Setup function for Sphinx extension"""
    app.add_directive('register', RegisterDirective)
    
    # Add CSS for color support - this creates a static CSS file
    def add_register_css(app, config):
        css_content = """
/* Register layout directive styles */
.register-layout {
    border-collapse: collapse;
    margin: 1em 0;
}

.register-header-row {
    background-color: #f0f0f0;
}

.register-bit-header,
.register-field-header {
    background-color: #e0e0e0;
    text-align: center;
    border: 1px solid #ccc;
    padding: 4px;
    font-weight: bold;
}

.register-field-data {
    border: 1px solid #ccc;
    padding: 8px;
    text-align: center;
}

.register-field-value {
    font-weight: bold;
    margin-bottom: 4px;
}

.register-field-name {
    font-size: 0.9em;
    color: #666;
    margin-top: 2px;
}

.register-field-name-only {
    font-size: 1em;
    color: #333;
}

.register-field-continuation {
    color: #999;
    font-style: italic;
}

/* Field descriptions table */
.register-descriptions {
    border-collapse: collapse;
    margin: 1em 0;
    width: 50%;
}

.register-desc-header {
    border: 1px solid #ccc;
    padding: 8px;
    background-color: #e0e0e0;
    text-align: center;
    font-weight: bold;
}

.register-desc-field-name {
    border: 1px solid #ccc;
    padding: 8px;
    vertical-align: top;
    background-color: #f8f8f8;
    width: 20%;
}

.register-desc-field-desc {
    border: 1px solid #ccc;
    padding: 8px;
    vertical-align: top;
    width: 80%;
}


    .register-field-header {
      font-weight: bold;
      color: #b6b6b6 !important;
      opacity: 0.8;
      background-color: #4a4ca0 !important;
      border: 1px solid #333466 !important;
      padding-top: 2px !important;
      padding-bottom: 2px !important;
      padding-left: 7px !important;
      padding-right: 7px !important;
    }

    .register-bit-header {
      font-weight: bold;
      color: #b6b6b6 !important;
      opacity: 0.8;
      background-color: #4a4ca0 !important;
      border: 1px solid #333466 !important;
      padding-top: 2px !important;
      padding-bottom: 2px !important;
      padding-left: 7px !important;
      padding-right: 7px !important;
    }

    .width-100 { width: 100% !important; }
    .width-200 { width: 200px !important; }
    .width-300 { width: 300px !important; }
    .width-400 { width: 400px !important; }
    .width-500 { width: 500px !important; }
    .width-600 { width: 600px !important; } 
    .width-700 { width: 700px !important; }
    .width-800 { width: 800px !important; }
    .width-900 { width: 900px !important; }
    .width-1000 { width: 1000px !important; }
    .width-1100 { width: 1100px !important; }
    .width-1200 { width: 1200px !important; }

/* Named color support */
.register-color-lightblue { background-color: lightblue !important; }
.register-color-lightgreen { background-color: lightgreen !important; }
.register-color-lightgray { background-color: lightgray !important; }
.register-color-lightyellow { background-color: lightyellow !important; }
.register-color-lightpink { background-color: lightpink !important; }
.register-color-lightcyan { background-color: lightcyan !important; }
.register-color-red { background-color: red !important; }
.register-color-green { background-color: green !important; }
.register-color-blue { background-color: blue !important; }
.register-color-yellow { background-color: yellow !important; }
.register-color-orange { background-color: orange !important; }
.register-color-purple { background-color: purple !important; }
.register-color-pink { background-color: pink !important; }
.register-color-cyan { background-color: cyan !important; }
.register-color-gray { background-color: gray !important; }
.register-color-white { background-color: white !important; }
.register-color-black { background-color: black !important; }

/* Hex colors - use CSS custom properties */
.register-field-data[data-register-color] {
    background-color: var(--register-bg-color, transparent);
}
"""
        
        # Write CSS to static directory
        import os
        static_path = os.path.join(app.outdir, '_static')
        os.makedirs(static_path, exist_ok=True)
        css_file = os.path.join(static_path, 'register-directive.css')
        with open(css_file, 'w') as f:
            f.write(css_content)
    
    # Add JavaScript to handle dynamic colors
    def add_register_js(app, config):
        js_content = """
document.addEventListener('DOMContentLoaded', function() {
    // Apply colors from data attributes
    const coloredCells = document.querySelectorAll('.register-field-data[data-register-color]');
    coloredCells.forEach(function(cell) {
        const color = cell.getAttribute('data-register-color');
        if (color) {
            cell.style.backgroundColor = color;
        }
    });
});
"""
        
        import os
        static_path = os.path.join(app.outdir, '_static')
        os.makedirs(static_path, exist_ok=True)
        js_file = os.path.join(static_path, 'register-directive.js')
        with open(js_file, 'w') as f:
            f.write(js_content)
    
    # Connect to the build process
    app.connect('config-inited', add_register_css)
    app.connect('config-inited', add_register_js)
    
    # Add the CSS and JS files
    app.add_css_file('register-directive.css')
    app.add_js_file('register-directive.js')
    
    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }


# If you need to use this directive from a directives folder:
# 
# 1. Save this file as: directives/register.py
# 
# 2. Create an __init__.py file in the directives folder:
#    # directives/__init__.py
#    from .register import setup as register_setup
#    
#    def setup(app):
#        register_setup(app)
#        return {
#            'version': '1.0',
#            'parallel_read_safe': True,
#            'parallel_write_safe': True,
#        }
#
# 3. In your conf.py, add:
#    import sys
#    import os
#    sys.path.insert(0, os.path.abspath('.'))
#    
#    extensions = [
#        'directives',  # This will import the directives package
#        # ... other extensions
#    ]