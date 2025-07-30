# Für jeden Step definieren wir nun zwei HTML‐Strings: description_html (links)
# und info_html (Popup-Text). Du kannst hier beliebige Tags wie <h2>, <b>, <ul>, <li> etc. verwenden.
from src.core.steps import Step

STEP_DESCRIPTIONS: dict[Step, tuple[str, str]] = {
    Step.UPLOAD: (
        # description_html
        """
        <h4>Step 1: Upload or Select File</h4>
        <p>
          Choose the file type you wish to upload: <b>Excel</b>, <b>CSV</b>, or <b>PDF</b>.
          Click <b>Browse…</b> to locate and load your file. Once the file appears as uploaded,
          click <b>Next</b> to continue.
        </p>
        """,
        # info_html
        """
        <h3>More about Step 1</h3>
        <p>
          In this step, you indicate which kind of file you want to work with and bring it into the system:
        </p>
        <ul>
          <li><b>Excel</b> (<code>.xlsx</code>, <code>.xls</code>)</li>
          <li><b>CSV</b> (<code>.csv</code>)</li>
          <li><b>PDF</b> (<code>.pdf</code>)</li>
        </ul>
        <p>
          After selecting a file, the application automatically recognizes its format and routes you to the appropriate workflow:
        </p>
        <ul>
          <li>For <b>Excel</b> files, you will choose a worksheet in the next step.</li>
          <li>For <b>PDF</b> files, you will proceed to select the table region.</li>
          <li>For <b>CSV</b> files, the data is loaded directly into the DataPrep module.</li>
        </ul>
        <p>
          When your file is successfully detected, click <b>Next</b> to move forward.
        </p>
        """,
    ),
    Step.PDF: (
        # description_html
        """
        <h4>Step 2: Select Table Region (PDF)</h4>
        <p>
          After uploading a PDF, navigate to the page containing your table. Click and drag
          to draw a red rectangle around the table. Then click <b>Extract Table</b>. Verify
          that all values appear correctly on the right, and click <b>Next</b> to continue.
        </p>
        """,
        # info_html
        """
        <h3>More about Step 2 (PDF)</h3>
        <p>
          Since PDFs do not automatically reveal table locations, you must manually select the area:
        </p>
        <ol>
          <li>Navigate to the PDF page with your table.</li>
          <li>Click and hold to start drawing a red selection box around the table region.</li>
          <li>Release the mouse button when the box fully covers the table, then click <b>Extract Table</b>.</li>
        </ol>
        <p>
          The system will run OCR on the selected area and display the extracted table on the right.
          Check that all values have been captured correctly—formatting issues can be addressed in the
          next view. Once satisfied, click <b>Next</b> to move on.
        </p>
        """,
    ),
    Step.WORKSHEET: (
        # description_html
        """
        <h4>Step 2: Choose Worksheet (Excel)</h4>
        <p>
          An Excel workbook has been detected. Select the worksheet (tab) that contains your data.
        </p>
        <p>
          From the list of sheet names, click the one you need, verify the preview, and then click <b>Next</b> to load it into DataPrep.
        </p>
        """,
        # info_html
        """
        <h3>More about Step 2 (Excel)</h3>
        <p>
          Excel workbooks often contain multiple sheets. In this step, you will see a list of all sheet names:
        </p>
        <ul>
          <li>Click the sheet name where your table is located.</li>
          <li>Check that the preview shows the correct columns and headers in real time.</li>
          <li>When you’ve confirmed it’s the right sheet, click <b>Next</b> to send it into DataPrep.</li>
        </ul>
        """,
    ),
    Step.DATAPREP: (
        # description_html
        """
        <h4>Step 3: Clean & Prepare Table (<i>DataPrep</i>)</h4>
        <p>
          In this step, you tidy up your raw data so that later filtering and mapping work correctly. You can:
        </p>
        <ul>
          <li>Select individual cells by clicking, select contiguous cells by clicking the first cell and Shift-clicking the second, or select non-contiguous cells by holding ⌘ (Command) while clicking multiple cells.</li>
          <li>Delete selected cells via right-click → <b>Cut</b> (⌘+X).</li>
          <li>Copy selected cells via right-click → <b>Copy</b> (⌘+C).</li>
          <li>Paste copied cells into selected areas via right-click → <b>Paste</b> (⌘+V). <i>(Note: The copied cells and the paste target must share the same relative layout.)</i></li>
        </ul>
        <p>
          Use the menu on the right to create or adjust selections:
        </p>
        <ul>
          <li><b>Every Nth Row</b> – highlights every nth row</li>
          <li><b>Shift by (Rows)</b> – shifts the currently highlighted nth rows up or down</li>
          <li><b>Every Nth Column</b> – highlights every nth column</li>
          <li><b>Shift by (Columns)</b> – shifts the currently highlighted nth columns left or right</li>
          <li><b>Mode:</b> <em>OR</em> or <em>AND</em> – determines whether a cell is marked if it meets at least one condition (OR) or must meet both row- and column-based criteria (AND)</li>
        </ul>
        <p>
          In the right menu, click <b>Apply</b> to turn a gray “preview” highlight into a solid blue selection. Use <b>Reset</b> to clear any selections made via the menu. Once cells are selected (blue), you can cut, copy, or delete them.
        </p>
        <p>
          You can also right-click on row or column headers to <b>Delete</b> or <b>Insert Row/Column</b> as needed.
        </p>
        """,
        # info_html
        """
        <h3>More about Step 3</h3>
        <p>
          DataPrep provides tools to eliminate inconsistencies and shape your data for the next filtering stage:
        </p>
        <ul>
          <li><b>Select Cells:</b> Single-click to pick one cell, Shift-click for a contiguous block, ⌘-click for multiple separate cells.</li>
          <li><b>Cut/Copy/Paste:</b> After selecting cells, right-click to cut (⌘+X), copy (⌘+C), or paste (⌘+V). Remember, the layout of the copied cells must match the target area exactly.</li>
          <li><b>Menu-Based Selections:</b>
            <ul>
              <li><b>Every Nth Row:</b> Specify a number to highlight every nth row.</li>
              <li><b>Shift by (Rows):</b> Move those highlighted rows up or down by a given offset.</li>
              <li><b>Every Nth Column:</b> Specify a number to highlight every nth column.</li>
              <li><b>Shift by (Columns):</b> Move those highlighted columns left or right.</li>
              <li><b>Mode:</b> <em>OR</em> (marks any cell fulfilling at least one criterion) or <em>AND</em> (marks only cells fulfilling both row- and column-criteria).</li>
            </ul>
          </li>
          <li><b>Reset & Apply:</b> When you configure a menu-based selection, it first appears in gray (a preview). Click <b>Apply</b> to turn it blue (active). Use <b>Reset</b> to clear the menu selections.</li>
          <li><b>Row/Column Operations:</b> Right-click on any row or column header to insert or delete an entire row/column.</li>
        </ul>
        <p>
          Once your table is cleaned—unwanted cells removed, columns renamed or reformatted, and any extra rows/columns handled—click <b>Next</b> to proceed to the <i>Filter</i> module.
        </p>
        """,
    ),
    Step.FILTER: (
        # description_html
        """
        <h4>Step 4: Select Columns & Apply Filters</h4>
        <p>
          Choose which columns should be present in the final output. Optionally
          enter a <i>Pandas‐style</i> filter expression to limit the rows.
        </p>
        <p>
          Example filter expressions:
        </p>
        <ul>
          <li><code>ColumnA > 100 and ColumnB == "XYZ"</code></li>
          <li><code>Age &lt; 30 or City == "Berlin"</code></li>
        </ul>
        """,
        # info_html
        """
        <h3>More about Step 4</h3>
        <p>
          In this step:
        </p>
        <ol>
          <li>Select the columns you want to keep.</li>
          <li>Optionally provide a condition to filter rows, for example:
            <ul>
              <li><code>Price &gt; 50</code> ⇒ only rows with Price greater than 50</li>
              <li><code>Status == "Active"</code> ⇒ only rows where Status is "Active"</li>
            </ul>
          </li>
          <li>Press <b>Validate</b> to check the filter, then click <b>Next</b>.</li>
        </ol>
        """,
    ),
    Step.GEODATA: (
        # description_html
        """
        <h4>Step 5: Apply GeoCSV Filters</h4>
        <p>
          If your data contains geographic coordinates or metadata you can
          define filters here to keep only a certain region (for example a bounding box).
        </p>
        <p>
          For instance, <code>latitude &gt; 50 and longitude &lt; 10</code> restricts
          the rows to a chosen area.
        </p>
        """,
        # info_html
        """
        <h3>More about Step 5</h3>
        <p>
          GeoCSV filters allow you to further constrain the geographic data:
        </p>
        <ul>
          <li>Bounding boxes defined by latitude and longitude.</li>
          <li>Filters based on region names like city or country.</li>
          <li>Other metadata such as country or postal code.</li>
        </ul>
        <p>
          Only the remaining rows will be used for the mapping step.
        </p>
        """,
    ),
    Step.MAPPING: (
        # description_html
        """
        <h4>Step 6: Prepare Automatic Mapping</h4>
        <p>
          The system tries to map your columns to geographic attributes
          automatically, for example mapping <code>City</code> to a geocoding database.
          Review the suggested matches before continuing.
        </p>
        """,
        # info_html
        """
        <h3>More about Step 6</h3>
        <p>
          Automatic mapping means:
        </p>
        <ol>
          <li>The system proposes a possible meaning for each column (such as City, Postal Code or Country).</li>
          <li>You check whether the mapping is correct.</li>
          <li>If something is wrong you can manually select the correct field type.</li>
        </ol>
        """,
    ),
    Step.MANUAL: (
        # description_html
        """
        <h4>Step 7: Confirm or Adjust Manual Mappings</h4>
        <p>
          Review the automatically created mapping. If a column was identified incorrectly
          you can assign the proper geographic attribute manually.
        </p>
        <p>
          Example: if the column <code>"ZipCode"</code> was mistakenly detected as <code>City</code>,
          manually choose <code>Postal Code</code> instead.
        </p>
        """,
        # info_html
        """
        <h3>More about Step 7</h3>
        <p>
          Here you can:
        </p>
        <ul>
          <li>Correct mistakes from the automatic mapping.</li>
          <li>Select the correct field type for each column, such as City, State or Country.</li>
          <li>Click <b>Next</b> when finished to move to the preview.</li>
        </ul>
        """,
    ),
    Step.PREVIEW: (
        # description_html
        """
        <h4>Step 8: Preview Map (Folium)</h4>
        <p>
          An interactive map preview shows how the cleaned and mapped points look
          on a map. Zoom, pan and click markers to view details.
        </p>
        """,
        # info_html
        """
        <h3>More about Step 8</h3>
        <p>
          The preview is built with <b>Folium</b> and allows:
        </p>
        <ul>
          <li>Map interaction: zooming, panning and clicking markers.</li>
          <li>Verification that all points appear in the expected locations.</li>
          <li>Troubleshooting: if a point is misplaced you can return to the mapping step.</li>
        </ul>
        """,
    ),
    Step.EXPORT: (
        # description_html
        """
        <h4>Step 9: Export Your Final Data</h4>
        <p>
          When you are satisfied with the preview choose the desired output
          format — <b>GeoJSON</b>, <b>CSV</b> or another supported type. The final
          file will then be offered for download.
        </p>
        """,
        # info_html
        """
        <h3>More about Step 9</h3>
        <p>
          Export options include:
        </p>
        <ul>
          <li><b>GeoJSON</b>: the standard for web mapping and many GIS tools.</li>
          <li><b>CSV</b>: plain tabular data without geometry.</li>
          <li>Additional formats (if implemented) such as Shapefile or KML.</li>
        </ul>
        <p>
          After selecting a format click <b>Export</b> to start the download.
        </p>
        """,
    ),
}
