using System.ComponentModel.DataAnnotations;

namespace weatherFrontEnd.Models{
    public class Log{
        public string email { get; set; }
        public string password { get; set; }
    }
    public class UserResponse{
        public int id { get; set; }
        public string email { get; set; }
        public string measurement { get; set; }
        public string defaultPage { get; set; }
    }
    public class AuthResponse{
        public System.DateTime expiry { get; set; }
        public string token { get; set; }
    }
    public class Pref{
        public string measurement { get; set; }
        public string defaultPage { get; set; }
    }
}
