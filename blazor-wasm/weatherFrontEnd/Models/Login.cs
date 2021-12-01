using System.ComponentModel.DataAnnotations;

namespace weatherFrontEnd.Models{
    public class Log{
        public string username { get; set; }
        public string password { get; set; }
    }
    public class UserResponse{
        public int id { get; set; }
        public string username { get; set; }
        public string email { get; set; }
    }
    public class AuthResponse{
        public DateTime expiry { get; set; }
        public string token { get; set; }
    }
}
