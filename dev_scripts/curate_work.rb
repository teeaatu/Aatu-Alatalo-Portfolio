require 'yaml'
require 'fileutils'

# 1. Work I = vari-ja-muoto.yml
v = YAML.load_file('_data/vari-ja-muoto.yml')
File.write('_data/work1.yml', v.to_yaml)

# 2. Work II = mustavalkoinen-sarja.yml
m = YAML.load_file('_data/mustavalkoinen-sarja.yml')
File.write('_data/work2.yml', m.to_yaml)

# 3. Work III = muiden yhdistelma
skip = ['recent.yml', 'work1.yml', 'work2.yml', 'categories.yml', 'etusivu.yml', 't.yml', 'vari-ja-muoto.yml', 'mustavalkoinen-sarja.yml', 'tapahtumat.yml', 'kuvaprojekti_ajasta_v365.yml', 'masters-2026.yml']

work3 = []
Dir.glob('_data/*.yml').each do |file|
  next if skip.include?(File.basename(file))
  
  data = YAML.load_file(file)
  next unless data.is_a?(Array)
  
  items = data.select { |i| i.is_a?(Hash) && i['kuva'] }
  work3.concat(items)
end

File.write('_data/work3.yml', work3.to_yaml)

puts "Work I size: #{v.size}"
puts "Work II size: #{m.size}"
puts "Work III size: #{work3.size}"
