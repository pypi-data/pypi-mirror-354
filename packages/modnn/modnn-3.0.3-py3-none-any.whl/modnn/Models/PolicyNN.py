import torch
import torch.nn as nn
import torch.autograd as autograd


class LSTM_encoder(nn.Module):

    def __init__(self, input_size, hidden_size, output_size, num_layers=1):
        super(LSTM_encoder, self).__init__()
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size,
                           num_layers=num_layers, batch_first=True, bias=True)
        self.Enfc = nn.Linear(in_features=hidden_size, out_features=output_size, bias=True)

    def forward(self, x_input):
        lstm_out, self.hidden = self.lstm(x_input)
        output = self.Enfc(lstm_out)

        return output, self.hidden

    def init_hidden(self, batch_size):
        return torch.zeros(self.num_layers, batch_size, self.hidden_size)

class LSTM_decoder(nn.Module):

    def __init__(self, input_size, hidden_size, output_size, num_layers=1):
        super(LSTM_decoder, self).__init__()
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size,
                           num_layers=num_layers, batch_first=True, bias=True)
        self.fc = nn.Linear(in_features=hidden_size, out_features=output_size, bias=True)

    def forward(self, x_input, encoder_hidden_states):
        lstm_out, self.hidden = self.lstm(x_input, encoder_hidden_states)
        output = self.fc(lstm_out)

        return output


class Policy(nn.Module):
    def __init__(self, args):
        super().__init__()
        para = args["para"]
        self.encoder = LSTM_encoder(input_size=para["en_policy_in"],
                                    hidden_size=para["en_policy_hidden"],
                                    output_size=para["en_policy_out"])
        self.decoder = LSTM_decoder(input_size=para["de_policy_in"],
                                    hidden_size=para["de_policy_hidden"],
                                    output_size=para["de_policy_out"])
        self.device = args['device']
        self.enLen = args['enLen']

    def forward(self, obs):
        """
        0.T_zone, 1.T_ambient, 2.solar, 3.day_sin, 4.day_cos,
        5.occ, 6.phvac, 7.setpt_cool, 8.setpt_heat, 9.price

        :param input_X:
        :return: u_opt (96 steps)
        """

        # Encoder
        Encoder_X = obs[:, :self.enLen, [0, 1, 2]]
        # Decoder
        Decoder_X = obs[:, self.enLen-1:-1, [1, 2, 5, 7, 8, 9]]
        encoder_out, encoder_hidden = self.encoder(Encoder_X)
        decoder_out = self.decoder(Decoder_X, encoder_hidden_states = encoder_hidden)

        return torch.tanh(decoder_out)
