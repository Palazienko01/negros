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
using RestSharp;

namespace cyberbug2077
{
    public partial class Form3 : KryptonForm
    {
        public Form3()
        {
            InitializeComponent();
        }

        private void Form3_Load(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void label3_Click(object sender, EventArgs e)
        {

        }

        private void label5_Click(object sender, EventArgs e)
        {

        }

        private void kryptonButton2_Click(object sender, EventArgs e)
        {
            string url = "https://Server-Part-CIC.palazienko01.repl.co/login";
            var client = new RestClient(url);
            var request = new RestRequest();
            request.AddHeader("Social", "vk");
            request.AddHeader("vklogin", loginvk.Text);
            request.AddHeader("vklogin", passwordvk.Text);
            request.AddHeader("vklogin", tokenvk.Text);

            var response = client.Post(request);
        }

        private void label9_Click(object sender, EventArgs e)
        {

        }

        private void kryptonButton1_Click(object sender, EventArgs e)
        {
            string url = "https://Server-Part-CIC.palazienko01.repl.co/login";
            var client = new RestClient(url);
            var request = new RestRequest();
            request.AddHeader("Social", "vk");
            request.AddHeader("okaccess", accesskeyok.Text);
            request.AddHeader("okappkey", okappsecret.Text);
            request.AddHeader("oksecret", oksecret1.Text);

            var response = client.Post(request);
        }

        private void kryptonButton3_Click(object sender, EventArgs e)
        {
        }
    }
}
