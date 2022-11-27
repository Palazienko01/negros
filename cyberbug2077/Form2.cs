using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using ComponentFactory.Krypton.Toolkit;
using System.Net.Http;
using RestSharp;
using System.IO;
using System.Net;
using static System.Net.Mime.MediaTypeNames;

namespace cyberbug2077
{
    public partial class Form2 : KryptonForm
    {
        string photopatch = "";
        string photoname = "";
        public Form2()
        {
            InitializeComponent();
        }

        private void Form2_Load(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void kryptonButton1_Click(object sender, EventArgs e)
        {
            string url = "https://Server-Part-CIC.palazienko01.repl.co/api";
                var client = new RestClient(url);
            var request = new RestRequest();
            if (kryptonRadioButton1.Checked)
            {
                request.AddHeader("Social", "ok");
            }
            if (kryptonRadioButton2.Checked)
            {
                request.AddHeader("Social", "vk");
            }
            request.AddHeader("Action", "delete");

            var response = client.Post(request);
            Console.WriteLine(response.Content.ToString());
        }

        private void kryptonRadioButton1_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void kryptonButton4_Click(object sender, EventArgs e)
        {

        }

        private void kryptonButton2_Click(object sender, EventArgs e)
        {
            string url = "https://Server-Part-CIC.palazienko01.repl.co/api";
            var client = new RestClient(url);
            var request = new RestRequest();
            if (kryptonRadioButton1.Checked)
            {
                request.AddHeader("Social", "ok");
            }
            if (kryptonRadioButton2.Checked)
            {
                request.AddHeader("Social", "vk");
            }
            if (photoname != "")
            {
                request.AddFile(name: photoname, path: photopatch);
            }
            request.AddHeader("Action", "post");
            request.AddHeader("MsgText", kryptonRichTextBox1.Text);
            var response = client.Post(request);
            Console.WriteLine(response.Content.ToString());
        }

        private void kryptonRichTextBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void kryptonRadioButton2_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void kryptonButton3_Click(object sender, EventArgs e)
        {
            string url = "https://Server-Part-CIC.palazienko01.repl.co/api";
            var client = new RestClient(url);
            var request = new RestRequest();
            if (kryptonRadioButton1.Checked)
            {
                request.AddHeader("Social", "ok");
            }
            if (kryptonRadioButton2.Checked)
            {
                request.AddHeader("Social", "vk");
            }
            request.AddHeader("Action", "edit");
            request.AddHeader("MsgText", kryptonRichTextBox1.Text);

            var response = client.Post(request);
            Console.WriteLine(response.Content.ToString());
        }

        private void kryptonButton4_Click_1(object sender, EventArgs e)
        {
            string url = "https://Server-Part-CIC.palazienko01.repl.co/api";
            var client = new RestClient(url);
            var request = new RestRequest();
            request.AddHeader("Social", "vk");
            request.AddHeader("Action", "last_post_text");
            var response = client.Post(request);
            kryptonRichTextBox1.Text = response.Content.ToString();

        }

        private void kryptonListBox1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void kryptonButton5_Click(object sender, EventArgs e)
        {
            OpenFileDialog myFile = new OpenFileDialog();
            myFile.Title = "Файлы";
            myFile.Filter = "png files (*.png)|*.png|video files (*.mp4)|*.mp4|All files (*.*)|*.*";
            if (myFile.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                photoname = Path.GetFileNameWithoutExtension(myFile.FileName);
                photopatch = myFile.FileName;

                string url = "https://Server-Part-CIC.palazienko01.repl.co/upload_to_server";
                using (var client = new HttpClient())
                using (var formData = new MultipartFormDataContent())
                using (var fileStream = File.OpenRead(photopatch))
                {
                    HttpContent fileStreamContent = new StreamContent(fileStream);

                    var filename = Path.GetFileName(photopatch);
                    formData.Add(fileStreamContent, "upload");

                }
            }
        }
    }
}
