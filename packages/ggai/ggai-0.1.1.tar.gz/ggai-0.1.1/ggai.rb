class ggai < Formula
  include Language::Python::Virtualenv

  desc "Helper for GeoGuessr training using OpenAI"
  homepage "https://github.com/rioriost/homebrew-ggai/"
  url "https://files.pythonhosted.org/packages/2a/28/cff82e49f973d6c7881ad0f1f4728ad378f00afcf05ad38feee962d57109/trmd-0.1.10.tar.gz"
  sha256 "5121168d983bd9eae656e667a392be57693099d946b64ef0b0c85fcd2784b03e"
  license "MIT"

  depends_on "python@3.10"

  def install
    virtualenv_install_with_resources
    system libexec/"bin/python", "-m", "pip", "install", "openai", "pyobjc"
  end

  test do
    system "#{bin}/ggai", "--help"
  end
end
