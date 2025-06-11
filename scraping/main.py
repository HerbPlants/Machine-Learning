from extract import extract_links
from transform import transform_data
from load import load_to_excel

if __name__ == "__main__":
    input_file = "link sisa 5.xlsx"
    output_file = "hasil_scraping.xlsx"

    link_df = extract_links(input_file)
    transformed_df = transform_data(link_df)

    load_to_excel(transformed_df, output_file)
    print("Saved to local Excel file:", output_file)