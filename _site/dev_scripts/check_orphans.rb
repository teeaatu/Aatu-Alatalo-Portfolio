require 'yaml'

recent = YAML.load_file('_data/recent.yml')

keep_urls = [
  'https://media.aatualatalo.com/Photographs/lapsetainola.webp',
  'https://media.aatualatalo.com/Photographs/misfortnute_2.webp',
  'https://media.aatualatalo.com/Photographs/nainenkahvilassa.webp',
  'https://media.aatualatalo.com/Photographs/lamppu.webp',
  'https://media.aatualatalo.com/Photographs/unto_valikatto.webp',
  'https://media.aatualatalo.com/Photographs/miesjaolut.webp'
]

# Extract basenames from keep_urls for matching, or just match exactly if kuva has https
keep_kuvas = keep_urls.map { |url| url }
keep_basenames = keep_urls.map { |url| File.basename(url) }

to_remove = []
recent.each do |item|
  kuva = item['kuva'].to_s
  basename = File.basename(kuva)
  unless keep_kuvas.include?(kuva) || keep_basenames.include?(basename)
    to_remove << item
  end
end

all_other_kuvas = []
Dir.glob('_data/*.yml').each do |f|
  next if f == '_data/recent.yml'
  data = YAML.load_file(f) rescue nil
  next unless data.is_a?(Array)
  data.each do |item|
    if item.is_a?(Hash) && item['kuva']
      all_other_kuvas << item['kuva']
      all_other_kuvas << File.basename(item['kuva'])
    end
  end
end

orphans = []
to_remove.each do |item|
  kuva = item['kuva'].to_s
  basename = File.basename(kuva)
  unless all_other_kuvas.include?(kuva) || all_other_kuvas.include?(basename)
    orphans << item
  end
end

puts "Items to remove from recent: #{to_remove.size}"
puts "Orphaned items: #{orphans.size}"
orphans.each { |o| puts " - #{o['kuva']}" }
