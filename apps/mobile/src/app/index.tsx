import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ActivityIndicator, KeyboardAvoidingView, Platform, ScrollView } from 'react-native';

export default function ScamShieldHome() {
  const [vpa, setVpa] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');
  const [language, setLanguage] = useState('english');

  const scanVpa = async () => {
    if (!vpa.trim()) {
      setError('Please enter a VPA');
      return;
    }
    
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/api/v1/scan/vpa', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          vpa: vpa.trim(),
          txn_type: 'pay',
          language: language
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setError('Failed to connect to the ScamShield API. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const getVerdictColor = (verdict: string) => {
    switch (verdict) {
      case 'green': return '#4caf50';
      case 'yellow': return '#ffeb3b';
      case 'red': return '#f44336';
      default: return '#9e9e9e';
    }
  };

  return (
    <KeyboardAvoidingView 
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <Text style={styles.headerTitle}>🛡️ ScamShield</Text>
        <Text style={styles.subtitle}>Verify who you are paying before you send money.</Text>

        <View style={styles.langContainer}>
          <TouchableOpacity 
            style={[styles.langBtn, language === 'english' && styles.langBtnActive]} 
            onPress={() => setLanguage('english')}
          >
            <Text style={[styles.langText, language === 'english' && styles.langTextActive]}>English</Text>
          </TouchableOpacity>
          <TouchableOpacity 
            style={[styles.langBtn, language === 'hindi' && styles.langBtnActive]} 
            onPress={() => setLanguage('hindi')}
          >
            <Text style={[styles.langText, language === 'hindi' && styles.langTextActive]}>हिन्दी</Text>
          </TouchableOpacity>
          <TouchableOpacity 
            style={[styles.langBtn, language === 'tamil' && styles.langBtnActive]} 
            onPress={() => setLanguage('tamil')}
          >
            <Text style={[styles.langText, language === 'tamil' && styles.langTextActive]}>தமிழ்</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            placeholder="Enter UPI ID (e.g., scam1@upi)"
            value={vpa}
            onChangeText={setVpa}
            autoCapitalize="none"
            autoCorrect={false}
          />
          <TouchableOpacity 
            style={styles.scanButton} 
            onPress={scanVpa}
            disabled={loading}
          >
            {loading ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.scanButtonText}>Scan VPA</Text>
            )}
          </TouchableOpacity>
        </View>

        {error ? <Text style={styles.errorText}>{error}</Text> : null}

        {result && (
          <View style={[styles.card, { borderTopColor: getVerdictColor(result.verdict) }]}>
            <View style={styles.cardHeader}>
              <Text style={[styles.verdictTitle, { color: getVerdictColor(result.verdict) }]}>
                {result.verdict.toUpperCase()}
              </Text>
              {result.safety_score !== null && (
                <Text style={styles.scoreText}>Score: {result.safety_score}/100</Text>
              )}
            </View>
            
            <Text style={styles.explanationText}>{result.explanation}</Text>
            
            {result.signals && result.signals.length > 0 && (
              <View style={styles.signalsContainer}>
                <Text style={styles.signalsHeader}>Detection Signals:</Text>
                {result.signals.map((sig: any, idx: number) => (
                  <Text key={idx} style={styles.signalItem}>
                    • {sig.code.replace(/_/g, ' ')} ({sig.severity})
                  </Text>
                ))}
              </View>
            )}
          </View>
        )}
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#121212',
  },
  scrollContainer: {
    flexGrow: 1,
    padding: 20,
    justifyContent: 'center',
  },
  headerTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#ffffff',
    textAlign: 'center',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#aaaaaa',
    textAlign: 'center',
    marginBottom: 20,
  },
  langContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginBottom: 30,
    gap: 10,
  },
  langBtn: {
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#444',
    backgroundColor: '#1e1e1e',
  },
  langBtnActive: {
    backgroundColor: '#3b82f6',
    borderColor: '#3b82f6',
  },
  langText: {
    color: '#aaa',
    fontSize: 14,
    fontWeight: 'bold',
  },
  langTextActive: {
    color: '#fff',
  },
  inputContainer: {
    flexDirection: 'row',
    marginBottom: 20,
  },
  input: {
    flex: 1,
    backgroundColor: '#1e1e1e',
    color: '#ffffff',
    borderWidth: 1,
    borderColor: '#333',
    borderRadius: 8,
    paddingHorizontal: 16,
    paddingVertical: 12,
    fontSize: 16,
    borderTopRightRadius: 0,
    borderBottomRightRadius: 0,
  },
  scanButton: {
    backgroundColor: '#3b82f6',
    paddingHorizontal: 20,
    justifyContent: 'center',
    alignItems: 'center',
    borderTopRightRadius: 8,
    borderBottomRightRadius: 8,
  },
  scanButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  errorText: {
    color: '#ef4444',
    textAlign: 'center',
    marginBottom: 16,
  },
  card: {
    backgroundColor: '#1e1e1e',
    borderRadius: 12,
    padding: 20,
    borderTopWidth: 6,
    marginTop: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 6,
    elevation: 8,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  verdictTitle: {
    fontSize: 24,
    fontWeight: '900',
    letterSpacing: 1,
  },
  scoreText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    backgroundColor: '#333',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  explanationText: {
    color: '#e0e0e0',
    fontSize: 16,
    lineHeight: 24,
    marginBottom: 16,
  },
  signalsContainer: {
    backgroundColor: '#121212',
    padding: 12,
    borderRadius: 8,
  },
  signalsHeader: {
    color: '#888',
    fontSize: 12,
    textTransform: 'uppercase',
    fontWeight: 'bold',
    marginBottom: 8,
  },
  signalItem: {
    color: '#bbb',
    fontSize: 14,
    marginBottom: 4,
  },
});
