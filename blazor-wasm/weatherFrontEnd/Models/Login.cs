using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace weatherFrontEnd.Models{
    public class Log{
        [Required]
        [EmailAddress(ErrorMessage = "Please enter a valid email address.")]
        [StringLength(60, ErrorMessage = "This email address is too long.")]
        public string username { get; set; }
        [Required]
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
    public class Passwd{
        [Required]
        public string old_password { get; set; }
        [Required]
        [MinLength(8, ErrorMessage = "Password must be at least 8 alphanumeric characters.")]
        public string new_password { get; set; }
    }
    public class Register{
        [Required]
        [EmailAddress(ErrorMessage = "Please enter a valid email address.")]
        [StringLength(60, ErrorMessage = "This email address is too long.")]
        public string email { get; set; }
        public string measurement { get; set; }
        public string defaultPage { get; set; }
        [Required]
        [MinLength(8, ErrorMessage = "Password must be at least 8 alphanumeric characters.")]
        public string password { get; set; }
        [Required]
        [CompareProperty("password", ErrorMessage = "The passwords do not match.")]
        [JsonIgnore]
        public string c_password { get; set; }
    }
}
