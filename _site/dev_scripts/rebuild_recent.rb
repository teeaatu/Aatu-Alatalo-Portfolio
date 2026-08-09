require 'yaml'

urls = [
  'https://media.aatualatalo.com/Photographs/lapsetainola.webp',
  'https://media.aatualatalo.com/Photographs/misfortnute_2.webp',
  'https://media.aatualatalo.com/Photographs/nainenkahvilassa.webp',
  'https://media.aatualatalo.com/Photographs/lamppu.webp',
  'https://media.aatualatalo.com/Photographs/unto_valikatto.webp',
  'https://media.aatualatalo.com/Photographs/miesjaolut.webp'
]

# gather all items from all yaml files
all_items = []
Dir.glob('_data/*.yml').each do |f|
  data = YAML.load_file(f) rescue nil
  if data.is_a?(Array)
    all_items.concat(data)
  end
end

new_recent = []
urls.each do |url|
  # find item
  item = all_items.find { |i| i.is_a?(Hash) && i['kuva'] == url }
  if item
    # keep a clean copy
    clean = item.dup
    clean.delete('pinned') # optional, maybe keep it? Let's just remove pinned from recent or keep it if it's there
    new_recent << clean
  else
    puts "NOT FOUND: #{url}"
  end
end

File.write('_data/recent.yml', new_recent.to_yaml)
