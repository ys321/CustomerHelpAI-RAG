-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Apr 13, 2025 at 03:33 PM
-- Server version: 8.0.31
-- PHP Version: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `legal_knowledge_base`
--

-- --------------------------------------------------------

--
-- Table structure for table `chat_history`
--

DROP TABLE IF EXISTS `chat_history`;
CREATE TABLE IF NOT EXISTS `chat_history` (
  `session_id` varchar(255) NOT NULL,
  `messages` text NOT NULL,
  PRIMARY KEY (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `kb_details`
--

DROP TABLE IF EXISTS `kb_details`;
CREATE TABLE IF NOT EXISTS `kb_details` (
  `id` int NOT NULL AUTO_INCREMENT,
  `kb_id` int NOT NULL,
  `step_order` int NOT NULL,
  `instruction` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_kb_id` (`kb_id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `kb_details`
--

INSERT INTO `kb_details` (`id`, `kb_id`, `step_order`, `instruction`) VALUES
(1, 101, 1, 'Restart your device and relaunch Netflix.'),
(2, 101, 2, 'Check your internet speed (minimum 3 Mbps for SD, 5 Mbps for HD).'),
(3, 101, 3, 'Log out and log back in to refresh your session.'),
(4, 101, 4, 'If the issue persists, clear cache or reinstall the app.'),
(5, 102, 1, 'Wait 15 minutes before trying again.'),
(6, 102, 2, 'Use the \'Forgot Password\' option to reset your login credentials.'),
(7, 102, 3, 'If the issue persists, contact support to unlock your account manually.'),
(8, 103, 1, 'Check if your card on file is expired or has insufficient funds.'),
(9, 103, 2, 'Update your payment method in the billing section.'),
(10, 103, 3, 'Retry the payment manually if needed.'),
(11, 103, 4, 'Wait a few minutes after updating for changes to take effect.'),
(12, 104, 1, 'Try changing the avatar from a different device.'),
(13, 104, 2, 'Log out and log back in to refresh the changes.'),
(14, 104, 3, 'Clear app cache or reload the web version.'),
(15, 105, 1, 'Ensure you’re entering the correct 4-digit PIN.'),
(16, 105, 2, 'Reset the PIN from the account settings if forgotten.'),
(17, 105, 3, 'Check if profile restrictions or maturity ratings are affecting access.'),
(18, 106, 1, 'Check your current plan to see how many streams are allowed.'),
(19, 106, 2, 'Stop streaming from one of the active devices.'),
(20, 106, 3, 'Upgrade your plan if you need more simultaneous streams.'),
(21, 107, 1, 'Check around your delivery area or with neighbors.'),
(22, 107, 2, 'Wait 24 hours—some carriers mark packages early.'),
(23, 107, 3, 'If still not received, report the issue from your Orders page or contact support.'),
(24, 108, 1, 'Confirm that the return was received by Amazon.'),
(25, 108, 2, 'Check the status of your refund in the Orders section.'),
(26, 108, 3, 'Refunds to credit cards may take 3–5 business days.'),
(27, 108, 4, 'If it\'s been longer, contact support with your order ID.'),
(28, 109, 1, 'Go to \'Your Orders\' and select \'Return or Replace\'.'),
(29, 109, 2, 'Choose \'Wrong item received\' as the reason.'),
(30, 109, 3, 'Print the return label and send it back.'),
(31, 109, 4, 'You’ll get a replacement or refund after return is processed.'),
(32, 110, 1, 'Restart your device and check your internet connection.'),
(33, 110, 2, 'Update the Prime Video app or reinstall it.'),
(34, 110, 3, 'Try streaming on another device to isolate the issue.'),
(35, 111, 1, 'Check if your card is expired or blocked.'),
(36, 111, 2, 'Update your payment method from the Wallet section.'),
(37, 111, 3, 'Try a different card or contact your bank.'),
(38, 112, 1, 'Go to ‘Your Orders’ and select the item.'),
(39, 112, 2, 'If the order is still processing, you’ll see an option to edit the address.'),
(40, 112, 3, 'Once shipped, you’ll need to contact the courier or cancel & reorder.');

-- --------------------------------------------------------

--
-- Table structure for table `kb_keywords`
--

DROP TABLE IF EXISTS `kb_keywords`;
CREATE TABLE IF NOT EXISTS `kb_keywords` (
  `id` int NOT NULL AUTO_INCREMENT,
  `kb_id` int NOT NULL,
  `keyword` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `kb_id` (`kb_id`),
  KEY `idx_keyword` (`keyword`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `kb_keywords`
--

INSERT INTO `kb_keywords` (`id`, `kb_id`, `keyword`) VALUES
(1, 101, 'can\'t play video'),
(2, 101, 'playback error'),
(3, 101, 'streaming not working'),
(4, 101, 'video stuck'),
(5, 101, 'netflix playback issue'),
(6, 102, 'account locked'),
(7, 102, 'login error'),
(8, 102, 'too many attempts'),
(9, 102, 'netflix login failed'),
(10, 102, 'reset account'),
(11, 103, 'payment failed'),
(12, 103, 'subscription not active'),
(13, 103, 'renewal issue'),
(14, 103, 'netflix payment problem'),
(15, 103, 'card declined'),
(16, 104, 'change avatar'),
(17, 104, 'profile picture not updating'),
(18, 104, 'netflix icon issue'),
(19, 104, 'avatar stuck'),
(20, 104, 'profile customization'),
(21, 105, 'pin not working'),
(22, 105, 'parental control broken'),
(23, 105, 'reset netflix pin'),
(24, 105, 'kids profile pin issue'),
(25, 105, 'can’t access profile'),
(26, 106, 'too many devices'),
(27, 106, 'can\'t stream'),
(28, 106, 'device limit netflix'),
(29, 106, 'upgrade plan'),
(30, 106, 'streaming blocked'),
(31, 107, 'order not received'),
(32, 107, 'package marked delivered'),
(33, 107, 'missing amazon order'),
(34, 107, 'delivery issue'),
(35, 107, 'tracking shows delivered'),
(36, 108, 'refund not received'),
(37, 108, 'amazon refund delay'),
(38, 108, 'return processed but no refund'),
(39, 108, 'money not credited'),
(40, 108, 'where is my refund'),
(41, 109, 'wrong item delivered'),
(42, 109, 'incorrect product'),
(43, 109, 'received something else'),
(44, 109, 'wrong order amazon'),
(45, 109, 'return wrong product'),
(46, 110, 'prime video not working'),
(47, 110, 'can\'t stream'),
(48, 110, 'amazon video buffering'),
(49, 110, 'prime video error'),
(50, 110, 'streaming issue'),
(51, 111, 'payment declined'),
(52, 111, 'card not working'),
(53, 111, 'order not processing'),
(54, 111, 'amazon card declined'),
(55, 111, 'update payment'),
(56, 112, 'change address'),
(57, 112, 'wrong delivery address'),
(58, 112, 'edit shipping address'),
(59, 112, 'update amazon order'),
(60, 112, 'shipping mistake');

-- --------------------------------------------------------

--
-- Table structure for table `kb_metadata`
--

DROP TABLE IF EXISTS `kb_metadata`;
CREATE TABLE IF NOT EXISTS `kb_metadata` (
  `id` int NOT NULL AUTO_INCREMENT,
  `kb_id` int NOT NULL,
  `meta_key` varchar(100) NOT NULL,
  `meta_value` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `kb_id` (`kb_id`),
  KEY `idx_meta_key` (`meta_key`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `kb_metadata`
--

INSERT INTO `kb_metadata` (`id`, `kb_id`, `meta_key`, `meta_value`) VALUES
(1, 101, 'audience', 'customer_service'),
(2, 101, 'priority', 'high'),
(3, 102, 'audience', 'customer_service'),
(4, 102, 'priority', 'medium'),
(5, 103, 'audience', 'customer_service'),
(6, 103, 'priority', 'high'),
(7, 104, 'audience', 'customer_service'),
(8, 104, 'priority', 'low'),
(9, 105, 'audience', 'customer_service'),
(10, 105, 'priority', 'medium'),
(11, 106, 'audience', 'customer_service'),
(12, 106, 'priority', 'medium'),
(13, 107, 'audience', 'customer_service'),
(14, 107, 'priority', 'high'),
(15, 108, 'audience', 'customer_service'),
(16, 108, 'priority', 'medium'),
(17, 109, 'audience', 'customer_service'),
(18, 109, 'priority', 'medium'),
(19, 110, 'audience', 'customer_service'),
(20, 110, 'priority', 'high'),
(21, 111, 'audience', 'customer_service'),
(22, 111, 'priority', 'medium'),
(23, 112, 'audience', 'customer_service'),
(24, 112, 'priority', 'medium');

-- --------------------------------------------------------

--
-- Table structure for table `knowledge_base`
--

DROP TABLE IF EXISTS `knowledge_base`;
CREATE TABLE IF NOT EXISTS `knowledge_base` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `intent` varchar(100) NOT NULL,
  `category` varchar(100) NOT NULL,
  `summary` text NOT NULL,
  `response_template` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `intent` (`intent`),
  KEY `idx_intent` (`intent`),
  KEY `idx_category` (`category`)
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `knowledge_base`
--

INSERT INTO `knowledge_base` (`id`, `title`, `intent`, `category`, `summary`, `response_template`) VALUES
(101, 'Streaming Issues - Playback Error', 'troubleshoot_playback_error', 'Streaming', 'Playback issues may occur due to device problems, slow internet, or account restrictions.', 'Sorry you\'re having trouble streaming! Please restart your device and check your internet speed. Try logging out and back in, or reinstalling the app if needed. Let me know if it continues!'),
(102, 'Account Locked - Too Many Login Attempts', 'account_locked_due_to_attempts', 'Account & Login', 'Your Netflix account may be temporarily locked due to multiple failed login attempts.', 'It looks like your account is temporarily locked due to too many login attempts. Please wait a few minutes and try again. You can also reset your password. Need help unlocking it? I’ve got you!'),
(103, 'Subscription Not Updating - Payment Issue', 'subscription_payment_issue', 'Billing', 'Payment issues can prevent your subscription from renewing successfully.', 'Looks like your subscription didn’t renew due to a payment issue. Please check your card details and update your payment method. You can retry the payment anytime. Let me know if you need a hand!'),
(104, 'Profile Customization - Avatar Not Updating', 'profile_avatar_update_issue', 'Profiles & Settings', 'Sometimes profile icons may not update due to cache or sync delays.', 'Your avatar might not be updating due to a sync delay. Try changing it from another device or logging out and back in. It should reflect soon—let me know if it doesn’t!'),
(105, 'Parental Controls - PIN Not Working', 'parental_control_pin_issue', 'Parental Controls', 'Parental control PINs may fail if incorrectly entered multiple times or out-of-sync with account settings.', 'Looks like the parental PIN isn’t working. Try resetting it from the account settings page. Double-check maturity settings too. I can help you reset it if needed!'),
(106, 'Device Limit Reached - Can\'t Stream', 'device_limit_reached', 'Streaming', 'Your Netflix plan may limit how many devices can stream simultaneously.', 'You’ve hit the device limit for your plan. Try stopping playback on another device, or consider upgrading your plan for more streams. Let me know how I can help!'),
(107, 'Order Not Delivered - Tracking Shows Delivered', 'order_not_received_but_marked_delivered', 'Orders & Delivery', 'Sometimes packages show as delivered but are not physically received due to courier errors or misplacement.', 'Sorry your package hasn’t arrived! Sometimes couriers mark deliveries early. Please check nearby or wait a few hours. If it\'s still missing, I’ll help you file a claim.'),
(108, 'Refund Not Received - Processing Delay', 'refund_processing_delay', 'Billing & Refunds', 'Refunds may take 3–5 business days after processing to reflect in your bank account.', 'Your refund might still be processing. It usually takes 3–5 business days to reflect. If it’s been longer, I’ll gladly check the status for you!'),
(109, 'Wrong Item Received', 'wrong_item_shipped', 'Orders & Delivery', 'If the wrong item was shipped, you can request a replacement or refund through the Orders section.', 'Sorry you got the wrong item! You can start a return or replacement from your Orders page. I’m here if you’d like me to walk you through it.'),
(110, 'Prime Video Not Streaming', 'prime_video_streaming_issue', 'Digital Services', 'Prime Video may not stream due to device issues, outdated app, or low internet speed.', 'Let’s fix your streaming issue! Please restart your device, check your Wi-Fi, and update or reinstall the Prime Video app. Still stuck? I’ll dig deeper with you!'),
(111, 'Payment Declined - Card Not Charged', 'payment_method_declined', 'Billing & Refunds', 'Your payment may be declined due to invalid details, insufficient funds, or card restrictions.', 'Your payment didn’t go through. Double-check your card details or try a different method. Need help updating your payment info? I’m here!'),
(112, 'Change Delivery Address After Placing Order', 'change_shipping_address', 'Orders & Delivery', 'You can change the delivery address if the order hasn’t shipped yet.', 'Need to update your delivery address? If your order hasn’t shipped, you can still change it in Your Orders. I can also help you cancel and re-order if needed!');

-- --------------------------------------------------------

--
-- Table structure for table `prompts`
--

DROP TABLE IF EXISTS `prompts`;
CREATE TABLE IF NOT EXISTS `prompts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `template` text NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `prompts`
--

INSERT INTO `prompts` (`id`, `name`, `template`, `is_active`, `created_at`) VALUES
(1, 'Custom Prompt', 'You are Customer Support assistant, a highly skilled and empathetic customer support agent powered by Add name in prompt. Use *only* the provided knowledge base context to answer the user\'s question.\n\nCONTEXT:\n{{context}}\n\nIf the context doesn’t provide a clear answer, say:  \n\"I don’t have enough information to answer that fully. Could you share more details?\"\n\nTHINKING:\n1. Understand user\'s intent and conversation history.\n2. Use the context to identify relevant information.\n3. If answer isn\'t obvious, ask one clarifying question.\n\nGUIDELINES:\n- Do NOT assume or fabricate any details.\n- Use friendly, natural, human tone (e.g., \"I can see how frustrating that must be\").\n- For vague replies like \"yes\", follow up based on the last known topic.\n- For inappropriate behavior, say: \"Your behaviour violates our guidelines!\"\n- For phone/help requests: \"Sorry, I can’t do that, but I’m happy to help via chat. For more, contact customersupport@gmail.com\"\n\nUser Message:\n{{question}}', 1, '2025-02-17 09:25:33');

-- --------------------------------------------------------

--
-- Table structure for table `token_usage`
--

DROP TABLE IF EXISTS `token_usage`;
CREATE TABLE IF NOT EXISTS `token_usage` (
  `id` int NOT NULL AUTO_INCREMENT,
  `session_id` varchar(255) NOT NULL,
  `input_tokens` int NOT NULL,
  `output_tokens` int NOT NULL,
  `total_tokens` int NOT NULL,
  `input_cost` decimal(10,4) NOT NULL,
  `output_cost` decimal(10,4) NOT NULL,
  `total_cost` decimal(10,4) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `kb_details`
--
ALTER TABLE `kb_details`
  ADD CONSTRAINT `kb_details_ibfk_1` FOREIGN KEY (`kb_id`) REFERENCES `knowledge_base` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `kb_keywords`
--
ALTER TABLE `kb_keywords`
  ADD CONSTRAINT `kb_keywords_ibfk_1` FOREIGN KEY (`kb_id`) REFERENCES `knowledge_base` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `kb_metadata`
--
ALTER TABLE `kb_metadata`
  ADD CONSTRAINT `kb_metadata_ibfk_1` FOREIGN KEY (`kb_id`) REFERENCES `knowledge_base` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
