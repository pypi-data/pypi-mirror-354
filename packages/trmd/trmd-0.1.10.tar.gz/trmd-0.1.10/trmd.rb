class Trmd < Formula
  include Language::Python::Virtualenv

  desc "Translate Markdown using OpenAI"
  homepage "https://github.com/rioriost/homebrew-trmd/"
  url "https://files.pythonhosted.org/packages/4f/62/55154fbcc18bdb2bb4620877303b604b8daaf20cf104c89bcb46c54aabb8/trmd-0.1.9.tar.gz"
  sha256 "0cbf80b730f995b7d5a4c75b6dcbbc2e703268636f6bb6b9747d1cbc5a4c483e"
  license "MIT"

  depends_on "python@3.13"

  def install
    virtualenv_install_with_resources
    system libexec/"bin/python", "-m", "pip", "install", "openai"
  end

  test do
    system "#{bin}/trmd", "--help"
  end
end
