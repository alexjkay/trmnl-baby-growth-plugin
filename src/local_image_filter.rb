require 'base64'

module LocalImageFilter
  IMAGE_NAME_PATTERN = /\A[a-z0-9]+(?:-[a-z0-9]+)*\z/

  def local_png_data_url(image_name)
    name = image_name.to_s
    raise ArgumentError, 'invalid local PNG name' unless IMAGE_NAME_PATTERN.match?(name)

    path = File.expand_path("../images/#{name}.png", __dir__)
    raise ArgumentError, "local PNG not found: #{name}" unless File.file?(path)

    "data:image/png;base64,#{Base64.strict_encode64(File.binread(path))}"
  end
end